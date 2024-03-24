from django.shortcuts import render
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.translation import gettext as _

#from GameSetup.models import GroupLogin
from .models import GroupCharacterSheet
from GameSetup.models import GameSettings
from GameSetup.views import check_start_time
from position.views import query_buyer_seller_number # pull in market balance function
import random

def generate_random_number(request):
    low, high = 1, 100  # Or any range you've defined
    number = random.randint(low, high)
    return JsonResponse({'number': number})

def group_character(request):
    #get teacher & class & group from session
    currentTeacher = request.session.get('currentTeacher')
    currentClassName = request.session.get('currentClassName')
    currentGroupNumber = request.session.get('currentGroup')
    #call the function to check game settings for this class
    result_from_check_start_time = check_start_time(currentTeacher, currentClassName, -1)
    # Extracting a value from the dictionary of results from function check_start_time
    rpg_closest_round = result_from_check_start_time['rpg_closest_round']
    #Use extracted value to query for this class this GROUP's data for this RPG round
    currentGroupCharacterSheet = GroupCharacterSheet.objects.filter(groupClass=currentClassName).filter(groupDigit=currentGroupNumber).filter(groupRPG=rpg_closest_round).first()

    # If the record doesn't exist, create it; First time for this group for this RPG to roll the dice
    if currentGroupCharacterSheet is None:
        currentGroupCharacterSheet = GroupCharacterSheet(
            groupClass = currentClassName, 
            groupDigit = currentGroupNumber, 
            groupRPG = rpg_closest_round, 
            groupDiceLeft = 5,  # Initialize with 5 rolls
            groupDiceLastRoll = 0  # Initialize with 0
        )
        currentGroupCharacterSheet.save()

    # Get count of buyers and sellers in the market to show in dice roll area
    buyers_count, sellers_count = query_buyer_seller_number(rpg_closest_round, currentClassName)

    context = {
        'groupDigit': currentGroupNumber,
        'currentClassName': currentClassName,
        'currentTeacher': currentTeacher,
        'groupRPG': rpg_closest_round,
        'groupDiceLeft': currentGroupCharacterSheet.groupDiceLeft,
        'groupDiceLastRoll': currentGroupCharacterSheet.groupDiceLastRoll,
        'groupResistancePrice': currentGroupCharacterSheet.groupResistancePrice,
        'groupFlex': currentGroupCharacterSheet.groupFlex,
        'groupMaxPurchase': currentGroupCharacterSheet.groupMaxPurchase,
        'groupDelivery': currentGroupCharacterSheet.groupDelivery,
        'groupUnits': currentGroupCharacterSheet.groupUnits,
        'groupImportance': currentGroupCharacterSheet.groupImportance,
        'groupQuality': currentGroupCharacterSheet.groupQuality,
        'groupNote': currentGroupCharacterSheet.groupNote,
        'groupRole': currentGroupCharacterSheet.groupRole,
        'buyers_count': buyers_count,
        'sellers_count':sellers_count,
    }
    context = {**result_from_check_start_time, **context}
    return render(request, 'dice_roll.html', context)


def roll_dice(request):
    if request.method == "POST":
        # Get the record
        try:
            # Retrieve this group's record for the current RPG round from the database
            #get teacher & class & group from session
            currentClassName = request.session.get('currentClassName')
            currentGroupNumber = request.session.get('currentGroup')
            currentTeacher = request.session.get('currentTeacher')
            #call the function to check game settings for this class
            result_from_check_start_time = check_start_time(currentTeacher, currentClassName, -1)
            # Extracting a value from the dictionary of results from function check_start_time
            rpg_closest_round = result_from_check_start_time['rpg_closest_round']
            diceLow = result_from_check_start_time['rpg_current_dice_low']
            diceHigh = result_from_check_start_time['rpg_current_dice_high']
            #Use GroupID extracted value to query for this class this GROUP's data for this RPG round
            currentGroupCharacterSheet = GroupCharacterSheet.objects.filter(groupClass=currentClassName, groupDigit=currentGroupNumber, groupRPG=rpg_closest_round).first()
        except GroupCharacterSheet.DoesNotExist:
            return JsonResponse({"status": "fail", "message": "Record not found"})

        # Check remaining rolls
        if currentGroupCharacterSheet.groupDiceLeft > 0:
            # Randomly select between low high dice
            roll_result = random.randint(diceLow, diceHigh)
            currentGroupCharacterSheet.groupDiceLeft -= 1
            currentGroupCharacterSheet.groupDiceLastRoll = roll_result
            # Randomly select between buyer 1 and seller -1
            currentGroupCharacterSheet.groupRole = random.choice([1, -1])

            if currentGroupCharacterSheet.groupDiceLeft == 4:  # The first dice roll after minus one above
                currentGroupCharacterSheet.groupFirstRoll = timezone.now() # For Research

            # Save the record
            currentGroupCharacterSheet.save()

            #fix the Buyer/Seller to text not integer
            #if currentGroupCharacterSheet.groupRole == -1:
            #    groupRole = 'SELLER'
            #elif currentGroupCharacterSheet.groupRole == 1:
            #    groupRole = 'Buyer'                        
            #else:
            #    groupRole = 'UNKNOWN'
            #end elseIf

            return JsonResponse({"status": "success", "rolls_left": currentGroupCharacterSheet.groupDiceLeft, "latest_roll": roll_result, "latest_role": currentGroupCharacterSheet.groupRole, "message": _("Roll sent to server.")})
        else:
            return JsonResponse({"status": "fail", "message": _("No rolls left")})


def update_attributes(request):
    if request.method == "POST":
        # Get the record
        try:
            # Retrieve this group's record for the current RPG round from the database
            #get teacher & class & group from session
            currentClassName = request.session.get('currentClassName')
            currentGroupNumber = request.session.get('currentGroup')
            currentTeacher = request.session.get('currentTeacher')
            #call the function to check game settings for this class
            result_from_check_start_time = check_start_time(currentTeacher, currentClassName, -1)
            # Extracting a value from the dictionary of results from function check_start_time
            rpg_closest_round = result_from_check_start_time['rpg_closest_round']
            #Use GroupID extracted value to query for this class this GROUP's data for this RPG round
            currentGroupCharacterSheet = GroupCharacterSheet.objects.filter(groupClass=currentClassName, groupDigit=currentGroupNumber, groupRPG=rpg_closest_round).first()
        except GroupCharacterSheet.DoesNotExist:
            return JsonResponse({"status": "fail", "message": _("Record not found")})

        currentGroupCharacterSheet.groupResistancePrice = request.POST.get('resistance')
        currentGroupCharacterSheet.groupFlex = request.POST.get('flex')
        currentGroupCharacterSheet.groupMaxPurchase = request.POST.get('purchase')
        currentGroupCharacterSheet.groupDelivery = request.POST.get('delivery')
        currentGroupCharacterSheet.groupUnits = request.POST.get('units')
        currentGroupCharacterSheet.groupImportance = request.POST.get('importance')
        currentGroupCharacterSheet.groupQuality = request.POST.get('quality')

        currentGroupCharacterSheet.groupPlayNow = timezone.now() # For research

        # Save the record
        currentGroupCharacterSheet.save()
        return JsonResponse({"status": "success"})
