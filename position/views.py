from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
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

from GameSetup.models import GroupLogin
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
from django.db.models import Max, F
import random
import math

# Create your views here.

#----------------------------BUILD MARKETPLACE HTML PAGE-------Admin ONLY-----------------
def position_marketplace(request): # called by the page position_marketplace.html on opening
    if request.session['admin_pass'] == 1: # First check if the administrator has a session PW pass
        context = position_marketplace_calculations(request, -1, -1) # Marketplace function; specify this is for MARKETPLACE page AND NO spcecific RPG round
        return render(request, 'position_marketplace.html', context)
    else:
        return redirect('home')

#----------------------------BUILD MARKETPLACE HTML PAGE FOR SPECIFIC RPG ROUND-------Admin ONLY----------
def position_marketplace_manual(request): # called by the page position_marketplace.html when dropdown for specific RPG round is choosen
    if request.session['admin_pass'] == 1: # First check if the administrator has a session PW pass
        rpg_choice = int(request.GET.get('rpg_choice', None)) # Get the specific RPG round chosen by user
        # This accounts for user did NOT click GO without choosing an RPG round number as the rpg_choice is -1 for NO choice
        context = position_marketplace_calculations(request, -1, rpg_choice) # Marketplace function; specify this is for MARKETPLACE page AND specific RPG round
        return render(request, 'position_marketplace.html', context)
    else:
        return redirect('home')

#----------------------------ADMIN GRADE PAGE FOR COPYING TO GOOGLE-------------------------

#----------------------------BUILD MARKETPLACE GRADE PAGE-------Admin ONLY-----------------
def position_result(request): # called by the page position_marketplace.html on opening
    if request.session['admin_pass'] == 1: # First check if the administrator has a session PW pass
        context = position_marketplace_calculations(request, -1, -1) # Marketplace function; specify this is for MARKETPLACE page AND NO spcecific RPG round
        return render(request, 'position_result.html', context)
    else:
        return redirect('home')

#----------------------------BUILD MARKETPLACE GRADE PAGE FOR SPECIFIC RPG ROUND-------Admin ONLY----------
def position_result_manual(request): # called by the page position_marketplace.html when dropdown for specific RPG round is choosen
    if request.session['admin_pass'] == 1: # First check if the administrator has a session PW pass
        rpg_choice = int(request.GET.get('rpg_choice', None)) # Get the specific RPG round chosen by user
        # This accounts for user did NOT click GO without choosing an RPG round number as the rpg_choice is -1 for NO choice
        context = position_marketplace_calculations(request, -1, rpg_choice) # Marketplace function; specify this is for MARKETPLACE page AND specific RPG round
        return render(request, 'position_result.html', context)
    else:
        return redirect('home')
#----------------------------------------END ADMIN PAGES--------------------------------

def position_buyer_seller_manual(request): # called by the page position_buyer_seller.html when dropdown for specific RPG round is choosen
    rpg_choice = int(request.GET.get('rpg_choice', None)) # Get the specific RPG round chosen by user
    # This accounts for user did NOT click GO without choosing an RPG round number as the rpg_choice is -1 for NO choice
    #context = position_marketplace_calculations(request, -1, rpg_choice) # Marketplace function; specify this is for MARKETPLACE page AND specific RPG round
    #return render(request, 'position_buyer_seller.html', context)
    

#----------------------------MARKETPLACE CALCULATIONS i.e. SCORES FOR ALL GROUPS-------
def position_marketplace_calculations(request, buyer_seller, rpg_manual_round): # 1 for buyer/seller page, buyer_seller=>-1 for marketplace, rpg_manual_round=>-1 for NO custom RPG round
    all_groups_results = [] # Holder to store all groups

    #get teacher & class from session
    currentTeacher = request.session.get('currentTeacher')
    currentClassName = request.session.get('currentClassName')

    #call the function to check game settings for this CLASS
    result_from_check_start_time = check_start_time(currentTeacher, currentClassName, rpg_manual_round)
    # Extracting a value from the dictionary of results from function check_start_time
    rpg_closest_round = int(result_from_check_start_time['rpg_closest_round'])

    #QUERY DB
    #Use extracted value to query for this class ALL GROUP's DiceRoll data for this RPG round
    #Each group will have ONE for the current RPG
    allGroupCharacterSheet = GroupCharacterSheet.objects.filter(groupClass=currentClassName).filter(groupRPG=rpg_closest_round)

    # Get count of buyers and sellers in the market
    buyers_count, sellers_count = query_buyer_seller_number(rpg_closest_round, currentClassName)

    # Initialize context outside of the loop incase an RPG round is manually selected but it has NO DEALS
    context = { # Supply values and an empty set value just in case
        'rpg_closest_round': rpg_closest_round,
        'currentTeacher': currentTeacher,
        'currentClassName': currentClassName,
        'allGroupCharacterSheet': allGroupCharacterSheet,
        'buyers_count': 0,
        'sellers_count': 0,
        'all_groups_results': []  # Set an empty list to start
    }

    all_group_deals_library = {} # Library holding list of deals for each group (initialze outside the for loop)
    #counting_library = {} # Library holding stuff to count across all groups

    # Loop through each group and calculate.
    for group in allGroupCharacterSheet:

        # Transform the values of quality & delivery to match THREE levels and not dice values
        group_role_name = 'none'
        if int(group.groupRole) == 1:
            transformed_quality = int(4 - ((group.groupQuality + 1) // 2))
            transformed_delivery = int(4 - ((group.groupDelivery + 1) // 2))
            group_role_name = 'Buyer'
        else:
            transformed_quality = int(((group.groupQuality + 1) / 2))
            transformed_delivery = int(((group.groupDelivery + 1) / 2))
            group_role_name = 'Seller'

        # Use the Flex Points from the dice results (no modification needed)
        flex_points = int(group.groupFlex)


        # Call functions
        #----------------------------CANCELED DEALS DB QUERY-------
        canceled_deals_count, repeated_cancels = query_cancel_db(rpg_closest_round, currentClassName, group.groupDigit)

        #-------------------CHECK DEAL AFFECTED BY CANCEL AND CALCULATE PENALTY----------------
        filtered_deals, penalized_deals, mutually_canceled_deals, all_deals, flex_points, repeated_deals = fetch_and_filter_deals(rpg_closest_round, currentClassName, group.groupDigit, canceled_deals_count, flex_points)
        
        #-------------------QUERY ALL DEALS LESS CANCELS----------------
        #if filtered_deals:
        final_deals, error_deals, waiting_for_counterpart, waiting_for_you, deal_quality_gap, deal_delivery_gap, deal_flex_points, flex_points = categorize_deals(filtered_deals, group.groupDigit, transformed_quality, transformed_delivery, flex_points, group.groupRole)

        all_group_deals_library[group] = final_deals # All the final deals for CURRENT group put into library with group number as KEY

        #-------------------CALCULATING INVENTORY NUMBERS----------------
        #if final_deals:
        total_units, final_deals, average_weighted, rpg_max_purchase, rpg_mod_units, resistance, rpg_fraction_close_to_max, rpg_fraction_close_to_mod = calculate_inventory_numbers(final_deals, group, group.groupRole, result_from_check_start_time)
        # Fix value formats to decimal
        rpg_fraction_close_to_max = Decimal(rpg_fraction_close_to_max)
        rpg_fraction_close_to_mod = Decimal(rpg_fraction_close_to_mod)
        resistance = round(Decimal(resistance), 2)
        average_weighted = round(Decimal(average_weighted), 2)

        #-------------------QUERY MESSAGES----------------
        all_messages = query_messages(rpg_closest_round, currentClassName, group.groupDigit)

        #--------------------Sum dice spent to check if locked in (PLAY NOW)---------------------------
        dice_spent = 0 # start/reset to zero
        # Add up some attributes to check dice spend. 
        dice_spent = group.groupResistancePrice + group.groupFlex + group.groupDelivery + group.groupUnits + group.groupImportance + group.groupQuality
        # If over 7 total, note the PlayNow has been clicked (i.e. the DiceRoll page uses the lower limit of 7)
        if dice_spent > 7:
            dice_spent_locked = 'LOCKED'
        else:
            dice_spent_locked = 'Running'

        #----------------------------FLEX POINTS CALCULATIONS-------
        # Get the Flex Point count from a function
        bonus_flex_points, flex_points, all_gifts, overproduction_flex_fee = calculate_flex_points(final_deals, rpg_mod_units, rpg_closest_round, currentClassName, group.groupDigit, flex_points, group.groupRole)

        # Calculate the score parts and total
        if filtered_deals: #only if some valid deals exist (as generated by function: fetch_and_filter_deals )
            if group.groupRole == 1: # The case of BUYER
                scoreA = Decimal(resistance) - Decimal(average_weighted)
            else: # The case of SELLER
                scoreA = Decimal(average_weighted) - Decimal(resistance)

            scoreB = scoreA / resistance
            scoreC = scoreB * 100
            scoreD = scoreC + flex_points
            scoreE = scoreD * group.groupImportance
            scoreFinal = scoreE * rpg_fraction_close_to_mod
            scoreFinal = round(scoreFinal, 2)
        else: # no filtered deals in query result assign zero values to show deals have not been made yet 
            scoreA = 0
            scoreB = 0
            scoreC = 0
            scoreD = scoreC + flex_points
            scoreE = scoreD * group.groupImportance
            bonus_flex_points = 0
            scoreFinal = -1

        # Collect the results for the current group.
        group_data = {
            'group_digit': group.groupDigit,
            'group_role': group.groupRole,
            'group_role_name': group_role_name,
            'resistance': resistance,
            'bonous_flex_points': bonus_flex_points,
            'scoreFinal': scoreFinal,
            'dice_left': group.groupDiceLeft,
            'last_roll': group.groupDiceLastRoll,
            'first_roll': group.groupFirstRoll,
            'play_now': group.groupPlayNow,
            'page_refresh': group.groupPageRefresh,
            'repeated_deals': len(repeated_deals),
            'repeated_cancels': len(repeated_cancels),
            'message_count': len(all_messages),
            'dice_spent_locked': dice_spent_locked,
        }
        all_groups_results.append(group_data)

        # Order the list by group number
        # Filter out items where 'group_digit' is None or doesn't exist
        all_groups_results = [item for item in all_groups_results if item.get('group_digit') is not None]
        # Now you can safely sort the list, if needed
        all_groups_results = sorted(all_groups_results, key=lambda x: x['group_digit'])

        # Order the DICTIONARY by group number
        # First filter out items where 'group_digit' is None or doesn't exist
        all_group_deals_library = {group: deals for group, deals in all_group_deals_library.items() if group.groupDigit is not None}
        # Sorting the dictionary by groupID
        all_group_deals_library = {k: v for k, v in sorted(all_group_deals_library.items(), key=lambda item: item[0].groupDigit)}

        context = {
            'rpg_closest_round': rpg_closest_round,
            'currentTeacher': currentTeacher,
            'currentClassName': currentClassName,
            'allGroupCharacterSheet': allGroupCharacterSheet,
            'all_groups_results': all_groups_results,
            'rpg_closest_end_date': result_from_check_start_time['rpg_closest_end_date'],
            'rpg_current_product_name': result_from_check_start_time['rpg_current_product_name'],
            'buyers_count': buyers_count,
            'sellers_count': sellers_count,
            'all_group_deals_library': all_group_deals_library,
            'dice_left': group.groupDiceLeft,
            'last_roll': group.groupDiceLastRoll,
        }
    
    if buyer_seller == 1: # Funciton argument passed from the buyer_seller function  (buyer_seller=>-1 for marketplace)
        return all_groups_results # Only return the scoring info for the group
    else: # Marketplace data
        #return render(request, 'position_marketplace.html', context)
        return context # Return all context variables for the calling function to build the html page marketplace 

#---------------------------------------BUILD POSITION_BUYER_SELLER HTML PAGE----------------------------------------
#setting up the initial page and placing useful variables into session
def position_buyer_seller(request):

    #@@@CLYDE this needs to get changed to not be session when all other stuff is working
    currentGroupNumber = int(request.session.get('currentGroup'))
    #get teacher & class from session
    currentTeacher = request.session.get('currentTeacher')
    currentClassName = request.session.get('currentClassName')


    # --------------------- Administrator opening this page from position_marketplace.html admin page -----------------------
    # TEST if this is the administrator who can choose ANY RPG or group to run
    #get the login teacher and className from URL
    currentGroupURL = request.GET.get('group') # Get the URL argument to check if administrator
    currentRoundURL = request.GET.get('RPG') # If Administrator get RPG round number

    if currentGroupURL and currentRoundURL and request.session['admin_pass'] == 1: # First check if the administrator has a session PW pass

        #Place Group and RPG Round into session
        request.session['currentGroup'] = currentGroupURL
        request.session['rpg_closest_round'] = currentRoundURL

        currentGroupNumber = int(currentGroupURL)
        rpg_closest_round = int(currentRoundURL)

        result_from_check_start_time = check_start_time(currentTeacher, currentClassName, rpg_closest_round)

    else:
        # Students starts here, i.e, students RUN this part-----------------

        #call the function to check game settings for this CLASS
        result_from_check_start_time = check_start_time(currentTeacher, currentClassName, -1)
        # Extracting a value from the dictionary of results from function check_start_time
        rpg_closest_round = int(result_from_check_start_time['rpg_closest_round'])
        
        # Add RPG Round to session
        request.session['rpg_closest_round'] = rpg_closest_round

    # END students RUN this part------------------------------------------

    #Use extracted value to query for this class this GROUP's data for this RPG round
    currentGroupCharacterSheet = GroupCharacterSheet.objects.filter(groupClass=currentClassName).filter(groupDigit=currentGroupNumber).filter(groupRPG=rpg_closest_round).first()
    # The above line does NOT exclude null groupNumber as the marketplace does because this is the group data (i.e., null user would not be here and page cannot run without current user)

    # Update the page refresh count for RESEARCH (ONLY for when students load page NOT counting administrator)
    if request.session['admin_pass'] != 1: # NOT administrator/teacher
        currentGroupCharacterSheet.groupPageRefresh += 1 # Fetch the current value and increment by 1
        currentGroupCharacterSheet.save() # Save the record

    # Transform the values of quality & delivery to match THREE levels and not dice values
    if int(currentGroupCharacterSheet.groupRole) == 1:
        transformed_quality = 4 - ((currentGroupCharacterSheet.groupQuality + 1) // 2)
        transformed_delivery = 4 - ((currentGroupCharacterSheet.groupDelivery + 1) // 2)
    else:
        transformed_quality = ((currentGroupCharacterSheet.groupQuality + 1) / 2)
        transformed_delivery = ((currentGroupCharacterSheet.groupDelivery + 1) / 2)

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
    canceled_deals_count, repeated_cancels = query_cancel_db(rpg_closest_round, currentClassName, currentGroupNumber)
    
#-------------------CHECK DEAL AFFECTED BY CANCEL AND CALCULATE PENALTY----------------
    filtered_deals, penalized_deals, mutually_canceled_deals, all_deals, flex_points, repeated_deals = fetch_and_filter_deals(rpg_closest_round, currentClassName, currentGroupNumber, canceled_deals_count, flex_points)

#-------------------QUERY ALL DEALS LESS CANCELS----------------
    #if filtered_deals:
    # Buyer/Seller have inverse relationship with the calculation done in this funciton, so for SELLER make a flag to signal inverse gap calculation in the function
    # Pass currentGroupCharacterSheet.groupRole to function
    final_deals, error_deals, waiting_for_counterpart, waiting_for_you, deal_quality_gap, deal_delivery_gap, deal_flex_points, flex_points = categorize_deals(filtered_deals, currentGroupNumber, transformed_quality, transformed_delivery, flex_points, currentGroupCharacterSheet.groupRole)

#-------------------CALCULATING INVENTORY NUMBERS----------------
    #if final_deals:
    total_units, final_deals, average_weighted, rpg_max_purchase, rpg_mod_units, resistance, rpg_fraction_close_to_max, rpg_fraction_close_to_mod = calculate_inventory_numbers(final_deals, currentGroupCharacterSheet, currentGroupCharacterSheet.groupRole, result_from_check_start_time)
    # Fix value formats to decimal
    rpg_fraction_close_to_max = round(Decimal(rpg_fraction_close_to_max), 2)
    average_weighted = round(Decimal(average_weighted), 2)

#-------------------QUERY MESSAGES----------------
    all_messages = query_messages(rpg_closest_round, currentClassName, currentGroupNumber)

#----------------------------FLEX POINTS CALCULATIONS-------
    # Get the Flex Point count from a function
    bonus_flex_points, flex_points, all_gifts, overproduction_flex_fee = calculate_flex_points(final_deals, rpg_mod_units, rpg_closest_round, currentClassName, currentGroupNumber, flex_points, currentGroupCharacterSheet.groupRole)


    # Calculate the score parts and total
    if filtered_deals: #only if some valid deals exist (as generated by fuction: fetch_and_filter_deals )
        if currentGroupCharacterSheet.groupRole == 1: # The case of BUYER
            scoreA = Decimal(resistance) - Decimal(average_weighted)
        else: # The case of SELLER
            scoreA = Decimal(average_weighted) - Decimal(resistance)

        scoreB = scoreA / Decimal(resistance)
        scoreC = scoreB * 100
        scoreD = scoreC + flex_points
        scoreE = scoreD * currentGroupCharacterSheet.groupImportance
        scoreFinal = scoreE * Decimal(rpg_fraction_close_to_mod)
    else:
        scoreA = 0
        scoreB = 0
        scoreC = 0
        scoreD = scoreC + flex_points
        scoreE = scoreD * currentGroupCharacterSheet.groupImportance
        scoreFinal = 0

#----------------------------GET MARKETPLACE ARRAY OF DATA-------    
    rpg_choice = int(request.GET.get('rpg_choice', rpg_closest_round))  # defaulting to RPG closest RPG round 1 IF no manual RPG choice.
    all_groups_results = position_marketplace_calculations(request, 1, rpg_choice) # specify this is for buyer_seller page; manual RPG round

    # Get count of buyers and sellers in the market
    buyers_count, sellers_count = query_buyer_seller_number(rpg_choice, currentClassName)
    #buyers_count, sellers_count = query_buyer_seller_number(rpg_manual_round, currentClassName)

    context = {
        'groupDigit': currentGroupNumber,
        'currentClassName': currentClassName,
        'currentTeacher': currentTeacher,
        'rpg_closest_round': rpg_closest_round,
        'buyers_count': buyers_count,
        'sellers_count': sellers_count,
        'final_deals': final_deals,
        'penalized_deals': penalized_deals,
        'mutually_canceled_deals': mutually_canceled_deals,
        'repeated_deals': repeated_deals,
        'repeated_cancels': repeated_cancels,
        'bonus_flex_points': bonus_flex_points,
        'overproduction_flex_fee': overproduction_flex_fee,
        'error_deals': error_deals,
        'groupDiceLeft': currentGroupCharacterSheet.groupDiceLeft,
        'groupDiceLastRoll': currentGroupCharacterSheet.groupDiceLastRoll,
        'groupResistancePrice': currentGroupCharacterSheet.groupResistancePrice,
        'groupFlex': currentGroupCharacterSheet.groupFlex,
        'rpgFlexPoints': flex_points,
        'groupMaxPurchase': currentGroupCharacterSheet.groupMaxPurchase,
        'groupDelivery': int(transformed_delivery),
        'groupUnits': currentGroupCharacterSheet.groupUnits,
        'groupImportance': currentGroupCharacterSheet.groupImportance,
        'groupQuality': int(transformed_quality),
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
        'rpg_fraction_close_to_mod': rpg_fraction_close_to_mod,
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
        'all_groups_results': all_groups_results,
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
def query_cancel_db(rpg_closest_round, currentClassName, group):

    # Query the CANCEL database for THIS GROUP's cancels (see below for an overall query)
    all_canceled_deals = cancel.objects.filter(groupRPG=rpg_closest_round, groupClass=currentClassName, groupDigit=group).values('groupDigit', 'dealDealID', 'dealCounterpart')


    # First, classify the cancels based on dealDealID, groupDigit, and dealCounterpart
    cancel_classification = defaultdict(int)  # This will store counts

    for canceled in all_canceled_deals:
        cancel_id = canceled['dealDealID']
        key = (cancel_id, canceled['groupDigit'], canceled['dealCounterpart'])
        cancel_classification[key] += 1

    # Now process each cancel and classify it as valid or repeated
    valid_cancels = []
    repeated_cancels = []

    for canceled in all_canceled_deals:
        cancel_id = canceled['dealDealID']
        key = (cancel_id, canceled['groupDigit'], canceled['dealCounterpart'])

        # If this specific combination has occurred more than once
        if cancel_classification[key] > 1:
            repeated_cancels.append(canceled)
            cancel_classification[key] -= 1  # Decrement the count
        else:
            valid_cancels.append(canceled)

    # The work above and below are not really related. CLYDE consider moving these into different functions
    # Query the CANCEL database to come up with the total LIST of cancels for later use
    all_canceled_deals = cancel.objects.filter(groupRPG=rpg_closest_round, groupClass=currentClassName).values('groupDigit', 'dealDealID', 'dealCounterpart')

    # Create a default dict to track canceled deals
    canceled_deals_count = defaultdict(lambda: {'count': 0, 'counterpart': None})

    for canceled in all_canceled_deals:
        deal_id = canceled['dealDealID']
        group_digit = canceled['groupDigit']
        counterpart = canceled['dealCounterpart']

        key = (deal_id, group_digit)
        canceled_deals_count[key]['count'] += 1
        canceled_deals_count[key]['counterpart'] = counterpart  # store counterpart
    
    return canceled_deals_count, repeated_cancels

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
    ).values('groupDigit','dealDealID', 'dealBuySell', 'dealCounterpart', 'dealQuality', 'dealDelivery', 'dealUnits', 'dealPrice', 'dealDateStamp')

    # FIRST REMOVE any deals that are using the same Deal ID over two matching deals
    # Step 1: Classify the deals based on their DealID and Buy/Sell.
    deal_classification = defaultdict(list)

    for deal in all_deals:
        deal_id = deal['dealDealID']
        deal_type = deal['dealBuySell']
        deal_classification[deal_id].append(deal_type)

    # Step 2: Filter out valid and invalid deals.
    valid_deals = []
    repeated_deals = []

    for deal in all_deals:
        deal_id = deal['dealDealID']
        deal_type = deal['dealBuySell']

        # Check if the deal_id has a valid buyer/seller combination.
        occurrences = deal_classification[deal_id]
        if occurrences.count(1) <= 1 and occurrences.count(-1) <= 1: # Checking for 1 occurance of buyer and 1 of seller
            valid_deals.append(deal)
        else:
            repeated_deals.append(deal)

            # Remove the deal from further consideration to retain only the first two.
            occurrences.remove(deal_type)
            if len(occurrences) == 0:
                del deal_classification[deal_id]

    all_deals = valid_deals  # Replace the original all_deals with the filtered valid deals.

    for deal in all_deals:
        deal_id = deal['dealDealID']
        group_digit = deal['groupDigit']
        dealCounterpart = deal['dealCounterpart']
        key1 = (deal_id, group_digit) # this deal's sender
        key2 = (deal_id, dealCounterpart) # this deal's counterpart

        cancel_count = 0 # reset the counter

        if key1 in canceled_deals_count: # Check if this deal's ID & group are in the cancels (The deal group is also a cancel group)
            cancel_counterpart = canceled_deals_count[key1]['counterpart'] # get the counterpart for this cancel
            if cancel_counterpart == dealCounterpart:
                cancel_count += 1  # This deal was canceled by this deal group (even the counterpart matches)
                # Now we want to see if there is a cancel that is the reverse of this one
                if key2 in canceled_deals_count: # Check if the counterpart has submitted a cancel for this deal
                    cancel_count += 1 # both this deal's group sender and counterpart have submitted cancel

        if cancel_count == 0:
            filtered_deals.append(deal)
        elif cancel_count == 1:
            # Delete from FLEX points here 0.5 Flex for 100 units only if the canceling group is the currentGroupNumber
            penalty_amount = (deal['dealUnits'] / 100) * .5
            if 0 < penalty_amount < 1: # Mimum fee of 1
                penalty_amount = 1
            else:
                penalty_amount = math.floor(penalty_amount) # Round DOWN
            deal['penalty_amount'] = penalty_amount
            flex_points -= penalty_amount  # Add the deduction to the overall Flex Point count
            penalized_deals.append(deal)  # Add to penalized_deals list regardless of who canceled
        elif cancel_count == 2:
            # Check if deal with the same dealDealID is already in the mutually_canceled_deals
            if not any(existing_deal['dealDealID'] == deal_id for existing_deal in mutually_canceled_deals):
                mutually_canceled_deals.append(deal)

    return filtered_deals, penalized_deals, mutually_canceled_deals, all_deals, flex_points, repeated_deals


#-------------------QUERY ALL DEALS LESS CANCELS----------------
def categorize_deals(filtered_deals, currentGroupNumber, transformed_quality, transformed_delivery, flex_points, groupRole):
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
            # Grab the first two deals regardless of how many there are
            deal1 = deals[0]
            deal2 = deals[1] if len(deals) > 1 else None

            if deal2:  # means there are at least two deals

                # Ensure deal1 is always for the current group
                if deal1['groupDigit'] != currentGroupNumber:
                    deal1, deal2 = deal2, deal1  # Swap the deals
            
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
                if int(deal1['dealCounterpart']) == int(currentGroupNumber):
                    waiting_for_you.append(deal1)
                else:
                    waiting_for_counterpart.append(deal1)

         # Create place in list and context and add up flex point changes from gaps in quality and delivery
        # Loop through each final deal to calculate the quality and delivery gaps
        for deal in final_deals:
            # Buyer/Seller are in oposite directions for flex gain/loss
            if groupRole == 1: # The case of BUYER
                deal_quality_gap = int(deal['dealQuality'] - transformed_quality)
                deal_delivery_gap = int(deal['dealDelivery'] - transformed_delivery)
            else: # The case of SELLER
                deal_quality_gap = int(transformed_quality - deal['dealQuality'])
                deal_delivery_gap = int(transformed_delivery - deal['dealDelivery'])

            # Add the gaps to the total flex points per 100 rounding up
            deal_flex_units = math.ceil(deal['dealUnits'] / 100)
            deal_flex_points = (deal_quality_gap + deal_delivery_gap) * deal_flex_units

            # Add the gain/loss of Flex to a session variable -----CLYDE I THINK THIS MAY NOT BE NEEDED ANY LONGER----------------
            flex_points += (deal_quality_gap + deal_delivery_gap) * deal_flex_units

            # Add the gaps to the deal list so you can use them in your template if needed
            deal['deal_quality_gap'] = deal_quality_gap
            deal['deal_delivery_gap'] = deal_delivery_gap
            deal['deal_flex_units'] = deal_flex_units
            deal['deal_flex_points'] = deal_flex_points

    return final_deals, error_deals, waiting_for_counterpart, waiting_for_you, deal_quality_gap, deal_delivery_gap, deal_flex_points, flex_points


#-------------------CALCULATING INVENTORY NUMBERS----------------
def calculate_inventory_numbers(final_deals, currentGroupCharacterSheet, groupRole, result_from_check_start_time):
    # Initialize variables for total units and total weighted, etc. These are needed to be returned.
    total_units = 0
    total_weighted = 0
    average_weighted = 0
    rpg_max_purchase = 0
    rpg_mod_units = 0
    resistance = 0
    rpg_fraction_close_to_max = 0

    # Calculate total units and total weighted
    for deal in final_deals:
        deal['weighted_price'] = deal['dealPrice'] * deal['dealUnits']
        total_units += deal['dealUnits']
        total_weighted += deal['weighted_price']

    # Calculate average of the weighted if total_units is not zero
    average_weighted = round((total_weighted / total_units) if total_units else 0, 2)

    # Calculate the resistance price and mod units
    # Use two indipendent matrix as buyer/seller are mixed up here
    attribute_value = 1
    if int(groupRole) == 1: # case of buyer
        resistance_levels = {
            2: 1.02,
            3: 1.03,
            4: 1.04,
            5: 1.05,
            6: 1.06
        }
        mod_levels = {
            2: 1.02,
            3: 1.03,
            4: 1.04,
            5: 1.05,
            6: 1.06
        }
    else: # case of seller
        resistance_levels = {
            2: .98,
            3: .96,
            4: .94,
            5: .92,
            6: .91
        }
        mod_levels = {
            2: 1.02,
            3: 1.03,
            4: 1.04,
            5: 1.05,
            6: 1.06
        }
    # Resistance Price calculation
    attribute_value = resistance_levels.get(currentGroupCharacterSheet.groupResistancePrice, 1)
    resistance = round(attribute_value * float(result_from_check_start_time['rpg_current_product_price']), 2)

    # Calculate modUnits based on attribute values
    attribute_value_units = mod_levels.get(currentGroupCharacterSheet.groupUnits, 1) # the points from dice
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

    rpg_max_purchase = int(attribute_value_max_purchase * rpg_mod_units) # This is in ADDITION to MOD UNITS ()

    if groupRole == -1: # If Seller


        rpg_fraction_close_to_mod = min(round(total_units / rpg_mod_units, 2), 1) # Caps anything over 1 (the LOWER target for SELLERs)
        rpg_fraction_close_to_max = round(total_units / rpg_max_purchase, 2) # This can go OVER the mod units target (paid for with Flex)

    else:  # Buyer (ONLY BUYER has the MAX hard limit to buy)
        rpg_fraction_close_to_mod = min(round(total_units / rpg_mod_units, 2), 1) # Caps anything over (the LOWER target for BUYERS)

        rpg_fraction_close_to_max = round(total_units / rpg_max_purchase, 2) # Does not cap for Buyer--shows OVER buying level

        if groupRole == 1 and rpg_fraction_close_to_max > 1: # The case of BUYER BANKRUPT if purchase over limit (seler has no problem)
            rpg_fraction_close_to_max = -1 # This should cause this RPG round score to be zero

    return total_units, final_deals, average_weighted, rpg_max_purchase, rpg_mod_units, resistance, rpg_fraction_close_to_max, rpg_fraction_close_to_mod

#-------------------QUERY MESSAGES----------------
def query_messages(rpg_closest_round, currentClassName, currentGroupNumber):
    all_messages = messaging.objects.filter(
        groupRPG=rpg_closest_round,
        groupClass=currentClassName
    ).filter(
        Q(groupDigit=currentGroupNumber) | 
        Q(messageReceiver=currentGroupNumber)
    ).values('groupDigit', 'messageReceiver', 'messageSubject', 'messageContent', 'messageDateStamp').order_by('-messageDateStamp') # order by timestamp in descending order

    return all_messages

#-------------------QUERY BUYER SELLER NUMBERS IN MARKET----------------
def query_buyer_seller_number(rpg_closest_round, currentClassName):

    # Get count of buyers and sellers by query all the group character sheets for current RPG round and class
    buyers_count = GroupCharacterSheet.objects.filter(groupClass=currentClassName).filter(groupRPG=rpg_closest_round).filter(groupRole=1).count()
    sellers_count = GroupCharacterSheet.objects.filter(groupClass=currentClassName).filter(groupRPG=rpg_closest_round).filter(groupRole=-1).count()

    return buyers_count, sellers_count

#----------------------------FLEX POINTS CALCULATIONS-------

def calculate_flex_points(final_deals, rpg_mod_units, rpg_closest_round, currentClassName, currentGroupNumber, flex_points, groupRole):
    # Initialize a dictionary to keep track of the units dealt with each group.
    units_by_group = defaultdict(int)
    units_total = 0 # Track total units to charge Seller for over production
    overproduction_flex_fee = 0

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

    # Seller over produces must spend 1 Flex per 10% over mod units
    if groupRole == -1: # Only applies to SELLER
        for deal in final_deals:
            units_total += deal['dealUnits']
        if units_total >= rpg_mod_units:
            overproduction_flex_fee = math.ceil((units_total - rpg_mod_units) / (rpg_mod_units * 0.1))

    # Buyer over buys, a hard fail; force overall score to zero

    # Calculate the final flex points
    flex_points = flex_points + flex_points_received - flex_points_sent + bonus_flex_points - overproduction_flex_fee
    return bonus_flex_points, flex_points, all_gifts, overproduction_flex_fee


#-----------------------CALCULATING SCORES SUPPORTING FUNCTIONS END  ---------------------------


#-----------------------DB INSERT/DELETE FUNCTIONS START---------------------------

# Deal form insert to DB
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

def remove_deal(request, deal_id):
    # Fetch all deals with the given dealDealID
    deals = responses.objects.filter(dealDealID=deal_id)

    if not deals:
        messages.error(request, f"Deal with ID {deal_id} does not exist.")
        return redirect('position_marketplace')

    # Iterate over each deal and update the RPG round number
    for deal in deals:
        deal.groupRPG += 100
        deal.save()

    messages.success(request, f"Deal {deal_id} was successfully updated.")

    # Get the RPG choice from the query parameters
    rpg_choice = request.GET.get('rpg_choice', None)

    # Generate the redirect URL. If rpg_choice is present, append it as a query parameter.
    redirect_url = reverse('position_marketplace')
    if rpg_choice:
        redirect_url += f"?rpg_choice={rpg_choice}"

    return redirect(redirect_url)  # Redirect back to the admin page with the optional RPG choice.


#-----------------------DB INSERT/DELETE FUNCTIONS END---------------------------


