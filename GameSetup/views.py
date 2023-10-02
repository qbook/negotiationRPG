from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime
from django.utils import timezone
from datetime import timedelta

# Create your views here.

from django.http import HttpResponse
from django.http import JsonResponse
from .models import GroupLogin
from .models import GameSettings
from .forms import GroupDigitForm
from .forms import GroupLoginForm





def home(request):
    # Clear all session variables to stop back arrow movement
    #request.session.clear()

    teachers = GameSettings.objects.all()
    groups = GroupLogin.objects.all()
    form = GroupDigitForm()
    context = {
        'teachers': teachers,
        'groups': groups,
        'form': form
    }
    return render(request, 'home.html', context)




#-------CLYDE THIS FUNCTION MAY NOT BE IN USE ANY LONGER----------------------
def login(request):
    #get the login teacher and className from URL
    currentTeacherURL = request.GET.get('teacher')
    currentClassNameURL = request.GET.get('className')
    currentGroupURL = request.GET.get('group')

    if currentGroupURL:
        currentGroup = GroupLogin.objects.filter(groupDigit=currentGroupURL).filter(groupClass=currentClassNameURL).first()
        context = {
            'currentGroup': currentGroup
        }
        #Place group and class name into session
        request.session['currentClassName'] = currentClassNameURL
        request.session['currentGroup'] = currentGroupURL
        #For group login, the teacher name is gotten from DB not URL
        request.session['currentTeacher'] = currentGroup.groupTeacher
    else:
        #CLYDE CHECK PW HERE OTHERWISE SEND BACK TO HOME
        #get the query result object
        currentTeacherClass = GameSettings.objects.filter(teacher=currentTeacherURL).filter(className=currentClassNameURL).first()
        context = {
            'currentTeacherClass': currentTeacherClass
        }
        #Place teacher and class name into session
        request.session['currentTeacher'] = currentTeacherURL
        request.session['currentClassName'] = currentClassNameURL
        request.session['currentClassPrimaryKey'] = currentTeacherClass.pk

    return render(request, 'login.html', context)


def setup(request):
    #get teacher & class from session
    currentTeacher = request.session.get('currentTeacher')
    currentClassName = request.session.get('currentClassName')

    #call the function to check game settings for this class
    result_from_check_start_time = check_start_time(currentTeacher, currentClassName)

    return render(request, 'setup.html', result_from_check_start_time)


def check_start_time(currentTeacher, currentClassName):
    #query for this teacher/class data
#    currentTeacherClass = GameSettings.objects.filter(teacher=currentTeacher).filter(className=currentClassName).first()
    currentTeacherClass = GameSettings.objects.filter(className=currentClassName).first()
    playDays = currentTeacherClass.playDays
    #get the closest ending date that has NOT passed yet
    #create a list of start dates
    rpg_start_dates = [
        currentTeacherClass.round0Start,
        currentTeacherClass.round1Start,
        currentTeacherClass.round2Start,
        currentTeacherClass.round3Start,
        currentTeacherClass.round4Start,
        currentTeacherClass.round5Start,
        currentTeacherClass.round6Start,
        currentTeacherClass.round7Start,
        currentTeacherClass.round8Start,
        currentTeacherClass.round9Start,
    ]
    #create a list of end dates
    rpg_end_dates = [
        currentTeacherClass.round0End,
        currentTeacherClass.round1End,
        currentTeacherClass.round2End,
        currentTeacherClass.round3End,
        currentTeacherClass.round4End,
        currentTeacherClass.round5End,
        currentTeacherClass.round6End,
        currentTeacherClass.round7End,
        currentTeacherClass.round8End,
        currentTeacherClass.round9End,
    ]
    #create a list of products
    rpg_product_names = [
        currentTeacherClass.round0ProductName,
        currentTeacherClass.round1ProductName,
        currentTeacherClass.round2ProductName,
        currentTeacherClass.round3ProductName,
        currentTeacherClass.round4ProductName,
        currentTeacherClass.round5ProductName,
        currentTeacherClass.round6ProductName,
        currentTeacherClass.round7ProductName,
        currentTeacherClass.round8ProductName,
        currentTeacherClass.round9ProductName,
    ]
    #create a list of product prices
    rpg_product_prices = [
        currentTeacherClass.round0ProductPrice,
        currentTeacherClass.round1ProductPrice,
        currentTeacherClass.round2ProductPrice,
        currentTeacherClass.round3ProductPrice,
        currentTeacherClass.round4ProductPrice,
        currentTeacherClass.round5ProductPrice,
        currentTeacherClass.round6ProductPrice,
        currentTeacherClass.round7ProductPrice,
        currentTeacherClass.round8ProductPrice,
        currentTeacherClass.round9ProductPrice,
    ]
    #create a list of product units
    rpg_product_units = [
        currentTeacherClass.round0ProductUnits,
        currentTeacherClass.round1ProductUnits,
        currentTeacherClass.round2ProductUnits,
        currentTeacherClass.round3ProductUnits,
        currentTeacherClass.round4ProductUnits,
        currentTeacherClass.round5ProductUnits,
        currentTeacherClass.round6ProductUnits,
        currentTeacherClass.round7ProductUnits,
        currentTeacherClass.round8ProductUnits,
        currentTeacherClass.round9ProductUnits,
    ]
    #create a list of product currency
    rpg_product_currencies = [
        currentTeacherClass.round0ProductCurrency,
        currentTeacherClass.round1ProductCurrency,
        currentTeacherClass.round2ProductCurrency,
        currentTeacherClass.round3ProductCurrency,
        currentTeacherClass.round4ProductCurrency,
        currentTeacherClass.round5ProductCurrency,
        currentTeacherClass.round6ProductCurrency,
        currentTeacherClass.round7ProductCurrency,
        currentTeacherClass.round8ProductCurrency,
        currentTeacherClass.round9ProductCurrency,
    ]

    #Use a timezone-aware now time
    now = timezone.now()
    # Filter out END dates that have already passed and then sort the list
    # This will create a list of tuples, each containing (index, datetime)
    rpg_future_dates = sorted([(index, dt) for index, dt in enumerate(rpg_end_dates) if (dt  + timedelta(playDays)) > now], key=lambda x: x[1])

    rpg_closest_end_date_tuple = rpg_future_dates[0] if rpg_future_dates else None
    if rpg_closest_end_date_tuple:
        rpg_closest_round, rpg_closest_end_date = rpg_closest_end_date_tuple
        #Use the index number to now get the START date from the list rpg_start_dates
        rpg_closest_start_date = rpg_start_dates[rpg_closest_round]
        #Use the index number to get current RPG product
        rpg_current_product_name = rpg_product_names[rpg_closest_round]
        #Use the index number to get current RPG product base price
        rpg_current_product_price = rpg_product_prices[rpg_closest_round]
        #Use the index number to get current RPG product base units
        rpg_current_product_units = rpg_product_units[rpg_closest_round]
        #Use the index number to get current RPG product currency
        rpg_current_product_currency = rpg_product_currencies[rpg_closest_round]
        #Get the dice values for low/high limits
        rpg_current_dice_high = currentTeacherClass.diceHigh
        rpg_current_dice_low = currentTeacherClass.diceLow


        #Get time to the END of the nearest play round
        rpg_play_days_left = rpg_closest_end_date + timedelta(currentTeacherClass.playDays)
        #Get the gap from now to the end of the roll time--some conversion needed to format well
        rpg_roll_time_left_gap = rpg_closest_end_date - now
        # Get the total seconds
        roll_gap_total_seconds = rpg_roll_time_left_gap.total_seconds()
        # Convert total_seconds into hours and minutes
        gap_hours = int(roll_gap_total_seconds // 3600)
        gap_minutes = int((roll_gap_total_seconds % 3600) // 60)
        rpg_roll_time_left = f"{gap_hours} hours, {gap_minutes} minutes"

    result = {
        'currentTeacherClass': currentTeacherClass,
        'currentClassName': currentClassName,
        'currentTeacher': currentTeacher,
        'rpg_closest_end_date': rpg_closest_end_date,
        'rpg_closest_round': rpg_closest_round,
        'rpg_closest_start_date': rpg_closest_start_date,
        'rpg_current_product_name': rpg_current_product_name,
        'rpg_current_product_price': rpg_current_product_price,
        'rpg_current_product_units': rpg_current_product_units,
        'rpg_current_product_currency': rpg_current_product_currency,
        'rpg_play_days_left': rpg_play_days_left,
        'rpg_roll_time_left': rpg_roll_time_left,
        'rpg_current_dice_low': rpg_current_dice_low,
        'rpg_current_dice_high': rpg_current_dice_high,
    }
    return result



def choose_group(request):

    # Try to get the className from POST data, else fall back to GET data
    currentClassNameURL = request.POST.get('className', request.GET.get('className'))
    
    # Get teacher name form the URL
    currentTeacherURL = request.POST.get('teacher', request.GET.get('teacher'))

    # Query the DB for list of groups in this class
    this_class_groups = GroupLogin.objects.filter(groupClass=currentClassNameURL)

    # Create a new form instance
    form = GroupLoginForm()
    
    # Create context
    context = {
        'this_class_groups': this_class_groups,
        'currentClassName': currentClassNameURL,
        'currentTeacher': currentTeacherURL,
        'form': form,
    }

    # Place class name into session
    request.session['currentClassName'] = currentClassNameURL
    # Place teacher name in session
    request.session['currentTeacher'] = currentTeacherURL

    # Check for POST request (form submission)
    if request.method == 'POST':
        form = GroupLoginForm(request.POST)
        if form.is_valid():
            # Do your password checking and redirecting here
            groupDigit = form.cleaned_data['groupDigit']
            groupPassword = form.cleaned_data['groupPassword']
            try: #problem here getting two at once
                group = GroupLogin.objects.get(groupDigit=groupDigit, groupClass=currentClassNameURL)
                #group = GroupLogin.objects.get(groupDigit=groupDigit)
                if group.groupPassword == groupPassword or groupPassword == "nchu_master_ta_2023": #allow a master PW
                    #Place group and class name into session
                    request.session['currentClassName'] = currentClassNameURL
                    request.session['currentGroup'] = groupDigit
                    return redirect('dice_roll')
                else:
                    context['error_message'] = "Wrong password."
            except GroupLogin.DoesNotExist:
                context['error_message'] = "Group does not exist."

    return render(request, 'choose_group.html', context)




def save_note(request):
    if request.method == 'POST':
        record_id = request.POST.get('record_id')
        note_value = request.POST.get('note')
        field_name = request.POST.get('field_name')
        try:        
            # Fetch the specific record from the database
            record = GameSettings.objects.get(pk=record_id)
            # Set the new value for the specified field
            setattr(record, field_name, note_value)
            # Save the changes
            record.save()
            return JsonResponse({'status': 'success'})
        except GameSettings.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Record not found'}) 


def about(request):
    return HttpResponse('<h1>ABOUT THE GAME</h1>')



