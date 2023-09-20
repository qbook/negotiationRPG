from django.shortcuts import render
from django.http import HttpResponseRedirect
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse

from decimal import Decimal
from django.db.models import Count
from collections import defaultdict

#from GameSetup.models import GroupLogin
from diceroll.models import GroupCharacterSheet
from GameSetup.models import GameSettings
from GameSetup.views import check_start_time
from position.forms import DealForm
from position.forms import CancelForm
from position.forms import GiftingForm
from position.forms import MessagingForm
from position.models import responses
from position.models import cancel
from position.models import gifting
from position.models import messaging
from position.models import cancel
from django.db.models import Q
from collections import defaultdict
import random
import math

# Create your views here.

#setting up the initial page and placing useful variables into session
def position_buyer_seller(request):

    #@@@CLYDE this needs to get changed to not be session when all other stuff is working
    currentGroupNumber = int(request.session.get('currentGroup'))


    #get teacher & class & group from session
    currentTeacher = request.session.get('currentTeacher')
    currentClassName = request.session.get('currentClassName')


    #call the function to check game settings for this CLASS
    result_from_check_start_time = check_start_time(currentTeacher, currentClassName)
    # Extracting a value from the dictionary of results from function check_start_time
    rpg_closest_round = int(result_from_check_start_time['rpg_closest_round'])
    
    #Use extracted value to query for this class this GROUP's data for this RPG round
    currentGroupCharacterSheet = GroupCharacterSheet.objects.filter(groupClass=currentClassName).filter(groupDigit=currentGroupNumber).filter(groupRPG=rpg_closest_round).first()

    # Transform the values of quality & delivery to match THREE levels and not dice values
    #@@@ Buyer vs Seller are inverted CLYDE watch out on this
    if int(currentGroupCharacterSheet.groupRole) == 1:
        transformed_quality = 4 - (currentGroupCharacterSheet.groupQuality // 2)
        transformed_delivery = 4 - (currentGroupCharacterSheet.groupDelivery // 2)
    else:
        transformed_quality = (currentGroupCharacterSheet.groupQuality // 2)
        transformed_delivery = (currentGroupCharacterSheet.groupDelivery // 2)

    # Use the Flex Points from the dice results (not modification needed)
    flex_points = int(currentGroupCharacterSheet.groupFlex)

#----------------------------SESSION VARIABLES SPECIAL CASES-------
    # Session varibles ONLY needed for individual group use of dashboard page NOT for teacher or market calcs
    # Run this FUNCTION to set what is needed
    session_set_variables(request, int(currentGroupCharacterSheet.groupRole))

#----------------------------GET FORMS FROM FORM.PY FILE-------    
    formDeal = DealForm  #the Send A Deal form to display is imported from forms.py
    formCancel = CancelForm  #the Send A Cancel form to display is imported from forms.py
    formGifting = GiftingForm #Sending Flex Points form imported from forms.py
    formMessaging = MessagingForm #Sending message form imported from forms.py
   

#----------------------------CANCELED DEALS DB QUERY-------
    canceled_deals_count = query_cancel_db(rpg_closest_round, currentClassName)
    

#-------------------CHECK DEAL AFFECTED BY CANCEL AND CALCULATE PENALTY----------------
    filtered_deals, penalized_deals, mutually_canceled_deals, all_deals, flex_points = fetch_and_filter_deals(rpg_closest_round, currentClassName, currentGroupNumber, canceled_deals_count, flex_points)


#-------------------QUERY ALL DEALS LESS CANCELS----------------
    #if filtered_deals:
    final_deals, error_deals, waiting_for_counterpart, waiting_for_you, deal_quality_gap, deal_delivery_gap, deal_flex_points = categorize_deals(filtered_deals, currentGroupNumber, transformed_quality, transformed_delivery, flex_points)


#-------------------CALCULATING INVENTORY NUMBERS----------------
    #if final_deals:
    total_units, final_deals, average_weighted, rpg_max_purchase, rpg_mod_units, resistance, rpg_fraction_close_to_max = calculate_inventory_numbers(final_deals, currentGroupCharacterSheet, result_from_check_start_time)


#-------------------QUERY MESSAGES----------------
    all_messages = query_messages(rpg_closest_round, currentClassName, currentGroupNumber)


#----------------------------FLEX POINTS CALCULATIONS-------
    # Get the Flex Point count from a function
    bonus_flex_points, flex_points, all_gifts = calculate_flex_points(final_deals, rpg_mod_units, rpg_closest_round, currentClassName, currentGroupNumber, flex_points)


    # Calculate the score parts and total
    if filtered_deals: #only if some valid deals exist (as generated by fuction: fetch_and_filter_deals )
        scoreA = Decimal(resistance) - Decimal(average_weighted)
        scoreB = scoreA / Decimal(resistance)
        scoreC = scoreB * 100
        scoreD = scoreC + flex_points
        scoreE = scoreD * currentGroupCharacterSheet.groupImportance
        scoreFinal = scoreE * Decimal(rpg_fraction_close_to_max)
    else:
        scoreA = 0
        scoreB = 0
        scoreC = 0
        scoreD = scoreC + flex_points
        scoreE = scoreD * currentGroupCharacterSheet.groupImportance
        scoreFinal = 0

    context = {
        'groupDigit': currentGroupNumber,
        'currentClassName': currentClassName,
        'currentTeacher': currentTeacher,
        'groupRPG': rpg_closest_round,
        #'canceled_deals': canceled_deals,
        'final_deals': final_deals,
        'penalized_deals': penalized_deals,
        'mutually_canceled_deals': mutually_canceled_deals,
        'bonus_flex_points': bonus_flex_points,

        'error_deals': error_deals,
        'groupDiceLeft': currentGroupCharacterSheet.groupDiceLeft,
        'groupDiceLastRoll': currentGroupCharacterSheet.groupDiceLastRoll,
        'groupResistancePrice': currentGroupCharacterSheet.groupResistancePrice,
        'groupFlex': currentGroupCharacterSheet.groupFlex,
        'rpgFlexPoints': flex_points,
        'groupMaxPurchase': currentGroupCharacterSheet.groupMaxPurchase,
        'groupDelivery': transformed_delivery,
        'groupUnits': currentGroupCharacterSheet.groupUnits,
        'groupImportance': currentGroupCharacterSheet.groupImportance,
        'groupQuality': transformed_quality,
        # These are in the group rpg model but are not being used I think CLYDE
        #'groupBasePrice': currentGroupCharacterSheet.groupBasePrice,
        #'groupBaseUnits': currentGroupCharacterSheet.groupBaseUnits,
        'groupNote': currentGroupCharacterSheet.groupNote,
        'groupRole': currentGroupCharacterSheet.groupRole,
        'formDeal': formDeal,
        'formCancel': formCancel,
        'formGifting': formGifting,
        'formMessaging': formMessaging,
        'waiting_for_counterpart': waiting_for_counterpart,
        'waiting_for_you': waiting_for_you,
        'deal_quality_gap': deal_quality_gap,
        'deal_delivery_gap': deal_delivery_gap,
        'deal_flex_points': deal_flex_points,
        'total_units': total_units,
        'average_weighted': average_weighted,
        'rpg_fraction_close_to_max': rpg_fraction_close_to_max,
        'rpg_mod_units': rpg_mod_units,
        'rpg_max_purchase': rpg_max_purchase,
        'rpg_resistance': resistance,
        'rpg_scoreA': round(scoreA, 2),
        'rpg_scoreB': round(scoreB, 2),
        'rpg_scoreC': round(scoreC, 2),
        'rpg_scoreD': round(scoreD, 2),
        'rpg_scoreE': round(scoreE, 2),
        'rpg_scoreFinal': round(scoreFinal, 2),
        'all_gifts': all_gifts,
        'all_messages': all_messages,
    }
    context = {**result_from_check_start_time, **context} #this is also sending the check_start_time view which is the RPG round settings
    return render(request, 'position_buyer_seller.html', context)

#---------------------------------------------------------------------------------------------------------------------
#-----------------------CALCULATING SCORES SUPPORTING FUNCTIONS START  ---------------------------


#----------------------------SESSION VARIABLES-------
# Session varibles ONLY needed for individual group use of dashboard page NOT for teacher or market calcs
def session_set_variables(request, group_role): # Set any session variable needed for individual group pages but NOT for teacher or marketplace
    request.session['groupRole'] = group_role

#----------------------------CANCELED DEALS DB QUERY-------
def query_cancel_db(rpg_closest_round, currentClassName):
    # Query the CANCEL database
    all_canceled_deals = cancel.objects.filter(
        groupRPG=rpg_closest_round,
        groupClass=currentClassName
    ).values('groupDigit', 'dealDealID')

    # Create a defaultdict to track canceled deals
    canceled_deals_count = defaultdict(int)

    for canceled in all_canceled_deals:
        deal_id = canceled['dealDealID']
        group_digit = canceled['groupDigit']
        canceled_deals_count[(deal_id, group_digit)] += 1
    return canceled_deals_count

#-------------------CHECK DEAL AFFECTED BY CANCEL AND CALCULATE PENALTY----------------
def fetch_and_filter_deals(rpg_closest_round, currentClassName, currentGroupNumber, canceled_deals_count, flex_points):
    # Initialize some variables
    filtered_deals = []
    penalized_deals = []
    mutually_canceled_deals = []

    # Query the DEAL database
    all_deals = responses.objects.filter(
        groupRPG=rpg_closest_round,
        groupClass=currentClassName
    ).filter(
        Q(groupDigit=currentGroupNumber) | 
        Q(dealCounterpart=currentGroupNumber)
    ).values('groupDigit','dealDealID', 'dealBuySell', 'dealCounterpart', 'dealQuality', 'dealDelivery', 'dealUnits', 'dealPrice')

    for deal in all_deals:
        deal_id = deal['dealDealID']
        group_digit = deal['groupDigit']
        cancel_count = canceled_deals_count.get((deal_id, group_digit), 0)
        
        if cancel_count == 0:
            filtered_deals.append(deal)
        elif cancel_count == 1:
            # Delete from FLEX points here 0.5 Flex for 100 units only if the canceling group is the currentGroupNumber
            if group_digit == currentGroupNumber:
                penalty_amount = (deal['dealUnits'] / 100) * .5
                penalty_amount = math.floor(penalty_amount)
                deal['penalty_amount'] = penalty_amount
                flex_points -= penalty_amount  # Add the deduction to the overall Flex Point count
            else:
                penalty_amount = 0  # No penalty if the canceling group is not currentGroupNumber
                deal['penalty_amount'] = penalty_amount
            penalized_deals.append(deal)  # Add to penalized_deals list regardless of who canceled
        elif cancel_count == 2:
            mutually_canceled_deals.append(deal)

    return filtered_deals, penalized_deals, mutually_canceled_deals, all_deals, flex_points


#-------------------QUERY ALL DEALS LESS CANCELS----------------
def categorize_deals(filtered_deals, currentGroupNumber, transformed_quality, transformed_delivery, flex_points):
    # Initialize some variables
    final_deals = []
    error_deals = []
    waiting_for_counterpart = []
    waiting_for_you = []
    deal_quality_gap = 0
    deal_delivery_gap = 0
    deal_flex_points = 0

    # Check that the query returned some deals
    if filtered_deals:
        deals_by_id = defaultdict(list)
        
        for deal in filtered_deals:  # only check those NOT removed due to cancels
            deal_id = deal['dealDealID']
            deals_by_id[deal_id].append(deal)

        for deal_id, deals in deals_by_id.items():
            if len(deals) > 1:
                deal1, deal2 = deals
                if ((deal1['dealBuySell'] == 1 and deal2['dealBuySell'] == -1) or
                        (deal1['dealBuySell'] == -1 and deal2['dealBuySell'] == 1)) and \
                        (deal1['dealUnits'] == deal2['dealUnits']) and (deal1['dealPrice'] == deal2['dealPrice']) and \
                        (deal1['dealQuality'] == deal2['dealQuality']) and (deal1['dealDelivery'] == deal2['dealDelivery']):
                    # This is a valid finalized deal (one buyer and one seller)
                    final_deals.append(deal1)  # place the first one into list (assumes the two deals match on every attribute)
                else:
                    # This is an error deal
                    error_deals.append(deal1)
                    error_deals.append(deal2)
            else:
                # Waiting for counterpart or you
                if len(deals) == 1:
                    deal = deals[0]
                    if int(deal['dealCounterpart']) == int(currentGroupNumber):
                        waiting_for_you.append(deal)
                    else:
                        waiting_for_counterpart.append(deal)

        # Create place in dictionary and context and add up flex point changes from gaps in quality and delivery
        # Loop through each final deal to calculate the quality and delivery gaps
        for deal in final_deals:
            deal_quality_gap = deal['dealQuality'] - transformed_quality
            deal_delivery_gap = deal['dealDelivery'] - transformed_delivery
            # Add the gaps to the total flex points per 100 rounding up
            deal_flex_units = math.ceil(deal['dealUnits'] / 100)
            deal_flex_points = (deal_quality_gap + deal_delivery_gap) * deal_flex_units

            # Add the gain/loss of Flex to a session variable
            flex_points += (deal_quality_gap + deal_delivery_gap) * deal_flex_units

            # Add the gaps to the deal dictionary so you can use them in your template if needed
            deal['deal_quality_gap'] = deal_quality_gap
            deal['deal_delivery_gap'] = deal_delivery_gap
            deal['deal_flex_units'] = deal_flex_units
            deal['deal_flex_points'] = deal_flex_points

    return final_deals, error_deals, waiting_for_counterpart, waiting_for_you, deal_quality_gap, deal_delivery_gap, deal_flex_points


#-------------------CALCULATING INVENTORY NUMBERS----------------
def calculate_inventory_numbers(final_deals, currentGroupCharacterSheet, result_from_check_start_time):
    # Initialize variables for total units and total weighted, etc. These are needed to be returned.
    total_units = 0
    total_weighted = 0
    average_weighted = 0
    rpg_max_purchase = 0
    rpg_mod_units = 0
    resistance = 0
    rpg_fraction_close_to_max = 0

    if final_deals:
        # Calculate total units and total weighted
        for deal in final_deals:
            deal['weighted_price'] = deal['dealPrice'] * deal['dealUnits']
            total_units += deal['dealUnits']
            total_weighted += deal['weighted_price']

        # Calculate average of the weighted if total_units is not zero
        average_weighted = round((total_weighted / total_units) if total_units else 0, 2)

        # Calculate the resistance price
        attribute_value = 1
        resistance_levels = {
            2: 1.02,
            3: 1.03,
            4: 1.04,
            5: 1.05,
            6: 1.06
        }
        attribute_value = resistance_levels.get(currentGroupCharacterSheet.groupResistancePrice, 1)

        resistance = round(attribute_value * float(result_from_check_start_time['rpg_current_product_price']), 2)
        resistance = f"{resistance:.2f}"

        # Calculate modUnits based on attribute values
        attribute_value_units = resistance_levels.get(currentGroupCharacterSheet.groupUnits, 1)
        rpg_mod_units = int(round(attribute_value_units * float(result_from_check_start_time['rpg_current_product_units'])))

        # Calculate maximum that can be purchased
        max_purchase_levels = {
            (1, 2): 1.1,
            (3, 4): 1.2,
            (5, 6): 1.3
        }
        attribute_value_max_purchase = 1
        for k, v in max_purchase_levels.items():
            if currentGroupCharacterSheet.groupMaxPurchase in range(k[0], k[1]+1):
                attribute_value_max_purchase = v
                break

        rpg_max_purchase = int(attribute_value_max_purchase * rpg_mod_units)
        rpg_fraction_close_to_max = min(round(total_units / rpg_mod_units, 2), 1)

    return total_units, final_deals, average_weighted, rpg_max_purchase, rpg_mod_units, resistance, rpg_fraction_close_to_max


#-------------------QUERY MESSAGES----------------
def query_messages(rpg_closest_round, currentClassName, currentGroupNumber):
    all_messages = messaging.objects.filter(
        groupRPG=rpg_closest_round,
        groupClass=currentClassName
    ).filter(
        Q(groupDigit=currentGroupNumber) | 
        Q(messageReceiver=currentGroupNumber)
    ).values('groupDigit', 'messageReceiver', 'messageSubject', 'messageContent')

    return all_messages

#----------------------------FLEX POINTS CALCULATIONS-------

def calculate_flex_points(final_deals, rpg_mod_units, rpg_closest_round, currentClassName, currentGroupNumber, flex_points):
    # Initialize a dictionary to keep track of the units dealt with each group.
    units_by_group = defaultdict(int)

    # Loop through each final deal to calculate units by group
    for deal in final_deals:
        group = deal['dealCounterpart']
        units_by_group[group] += deal['dealUnits']

    # Initialize bonus flex points
    bonus_flex_points = 0

    # Check which groups meet the 10% criteria.
    for group, units in units_by_group.items():
        if units >= 0.1 * rpg_mod_units:
            bonus_flex_points += 1

    # Query the gifting model
    all_gifts = gifting.objects.filter(
        groupRPG=rpg_closest_round,
        groupClass=currentClassName
    ).filter(
        Q(groupDigit=currentGroupNumber) | 
        Q(giftReceiver=currentGroupNumber)
    ).values('groupDigit', 'giftReceiver', 'giftAmount', 'giftMessage')

    # Initialize variables for flex points sent and received
    flex_points_sent = 0
    flex_points_received = 0

    # Calculate points sent and received from gifts
    for gift in all_gifts:
        if gift['groupDigit'] == currentGroupNumber:
            flex_points_sent += gift['giftAmount']
        if gift['giftReceiver'] == currentGroupNumber:
            flex_points_received += gift['giftAmount']

    # Calculate the final flex points
    flex_points = flex_points + flex_points_received - flex_points_sent + bonus_flex_points

    return bonus_flex_points, flex_points, all_gifts


#-----------------------CALCULATING SCORES SUPPORTING FUNCTIONS END  ---------------------------


#-----------------------DB INSERT FUNCTIONS START---------------------------

#Deal form insert to DB
def save_deal(request):
    if request.method == 'POST':
        form = DealForm(request.POST)
        if form.is_valid():

            #get values from session variables
            currentGroupNumber = request.session.get('currentGroup')
            currentClassName = request.session.get('currentClassName')
            rpg_closest_round = request.session.get('rpg_closest_round')
            groupRole = request.session.get('groupRole')

            deal = responses(
                groupDigit=currentGroupNumber,
                groupClass=currentClassName,
                groupRPG=rpg_closest_round,
                dealDateStamp=timezone.now(),
                dealDealID=form.cleaned_data['dealID'],
                dealCounterpart=form.cleaned_data['counterparty'],
                dealBuySell=groupRole,
                dealUnits=form.cleaned_data['units'],
                dealPrice=form.cleaned_data['price'],
                dealQuality=form.cleaned_data['quality'],
                dealDelivery=form.cleaned_data['delivery'],
            )
            deal.save()

            messages.success(request, "Deal saved.")
            return HttpResponseRedirect('/position_buyer_seller/')

        else:
            messages.error(request, "Form is not valid.")
            return HttpResponseRedirect('/position_buyer_seller/')

    else:
        messages.error(request, "Method not allowed.")
        return HttpResponseRedirect('/position_buyer_seller/')


# Cancel Deal form insert to DB
def cancel_deal(request):
    if request.method == 'POST':
        form = CancelForm(request.POST)
        if form.is_valid():

            #get values from session variables
            currentGroupNumber = request.session.get('currentGroup')
            currentClassName = request.session.get('currentClassName')
            rpg_closest_round = request.session.get('rpg_closest_round')

            deal = cancel(
                groupDigit=currentGroupNumber,
                groupClass=currentClassName,
                groupRPG=rpg_closest_round,
                dealDateStamp=timezone.now(),
                dealDealID=form.cleaned_data['dealIDCancel'],
                dealCounterpart=form.cleaned_data['counterpartyCancel'],
            )
            deal.save()

            messages.success(request, "Cancel of deal saved.")
            return HttpResponseRedirect('/position_buyer_seller/')
        else:
            messages.error(request, "Form is not valid.")
            return HttpResponseRedirect('/position_buyer_seller/')
    else:
        messages.error(request, "Method not allowed.")
        return HttpResponseRedirect('/position_buyer_seller/')


# Gift Flex Points form insert to DB
def gift_flex(request):
    if request.method == 'POST':
        form = GiftingForm(request.POST)
        if form.is_valid():
            #get values from session variables
            currentGroupNumber = request.session.get('currentGroup')
            currentClassName = request.session.get('currentClassName')
            rpg_closest_round = request.session.get('rpg_closest_round')

            gift = gifting(
                groupDigit=currentGroupNumber,
                groupClass=currentClassName,
                groupRPG=rpg_closest_round,
                giftDateStamp=timezone.now(),
                giftReceiver=form.cleaned_data['giftReceiver'],
                giftAmount=form.cleaned_data['giftAmount'],
                giftMessage=form.cleaned_data['giftMessage'],
            )
            gift.save()

            messages.success(request, "Gift sent.")
            return HttpResponseRedirect('/position_buyer_seller/')
        else:
            messages.error(request, "Form is not valid.")
            return HttpResponseRedirect('/position_buyer_seller/')
    else:
        messages.error(request, "Method not allowed.")
        return HttpResponseRedirect('/position_buyer_seller/')


# Send Message form insert to DB
def send_message(request):
    if request.method == 'POST':
        form = MessagingForm(request.POST)
        if form.is_valid():
            #get values from session variables
            currentGroupNumber = request.session.get('currentGroup')
            currentClassName = request.session.get('currentClassName')
            rpg_closest_round = request.session.get('rpg_closest_round')

            message = messaging(
                groupDigit=currentGroupNumber,
                groupClass=currentClassName,
                groupRPG=rpg_closest_round,
                messageDateStamp=timezone.now(),
                messageReceiver=form.cleaned_data['messageReceiver'],
                messageSubject=form.cleaned_data['messageSubject'],
                messageContent=form.cleaned_data['messageContent'],
            )
            message.save()

            messages.success(request, "Message sent.")
            return HttpResponseRedirect('/position_buyer_seller/')
        else:
            messages.error(request, "Form is not valid.")
            return HttpResponseRedirect('/position_buyer_seller/')
    else:
        messages.error(request, "Method not allowed.")
        return HttpResponseRedirect('/position_buyer_seller/')

#-----------------------DB INSERT FUNCTIONS END---------------------------


