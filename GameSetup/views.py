from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse
from django.http import JsonResponse
from .models import GroupLogin
from .models import GameSettings
from .forms import GroupDigitForm
from .forms import GroupLoginForm
from .forms import GroupSettingsForm
from .forms import GameSettingsForm
from .models import GroupLogin
from django.contrib import messages
from .models import StudentList
from django.utils.translation import gettext as _
from .forms import CSVUploadForm

import csv

# Create your views here.

def upload_csv(request):
    # get teacher & class from session
    currentTeacher = request.session.get('currentTeacher')
    currentClassName = request.session.get('currentClassName')
    class_members = StudentList.objects.filter(
        className=currentClassName,
    ).values('chineseName', 'englishName', 'studentNumber', 'groupDigit').order_by('groupDigit', 'studentNumber')

    # Create a new form instance
    form = CSVUploadForm()
    
    # Create context early to also add message for rendering in the template
    context = {
        'form': form,
        'currentTeacher': currentTeacher,
        'currentClassName': currentClassName,
        'class_members': class_members,
    }

    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        import csv
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n") # End of line

            # Skip the first two rows
            for line in lines[2:]:                        
#                fields = line.split(",")
                fields = line.split("\t") # Use TAB to serperate columns

                if len(fields) == 4:  # Ensuring there are exactly 4 columns
                    _, created = StudentList.objects.update_or_create(
                        studentNumber=fields[0],
                        chineseName=fields[1],
                        englishName=fields[2],
                        groupDigit=fields[3],
                        className=currentClassName  # Set className from the session variable
                    )
            # return HttpResponse("CSV file has been imported")
            # Add a success message
            messages.success(request, 'Data imported successfully!')
            return redirect('position_marketplace')

    # If not POST, then it's a GET request, so create a blank form
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', context)


def home(request):
    # CLYDE this caused login problems--may need to do a check FIRST if variables are already in session before clearing
    # Clear all session variables to stop back arrow movement
    #request.session.clear()

    teachers = GameSettings.objects.all().order_by('-lastUpdate')  # Assuming the field is named 'created'
    groups = GroupLogin.objects.all()  # Assuming the field is named 'created'
    form = GroupDigitForm()
    context = {
        'teachers': teachers,
        'groups': groups,
        'form': form
    }
    return render(request, 'home.html', context)

#-------CLYDE THIS FUNCTION MAY NOT BE IN USE ANY LONGER----------------------START
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
# END-------CLYDE THIS FUNCTION MAY NOT BE IN USE ANY LONGER----------------------END

def setup(request):
    #get teacher & class from session
    currentTeacher = request.session.get('currentTeacher')
    currentClassName = request.session.get('currentClassName')

    #call the function to check game settings for this class
    result_from_check_start_time = check_start_time(currentTeacher, currentClassName)

    return render(request, 'setup.html', result_from_check_start_time)


def check_start_time(currentTeacher, currentClassName, rpg_manual_round):
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

    # Check if looking for CLOSEST non-passed RPG or MANUAL user-chosen RPG round
    if rpg_manual_round != -1:  # If user chooses a specific RPG round
        rpg_future_dates = sorted([(index, dt) for index, dt in enumerate(rpg_end_dates)], key=lambda x: x[1])
        rpg_closest_end_date_tuple = rpg_future_dates[rpg_manual_round] if rpg_future_dates else (0, rpg_end_dates[0]) # grab the FIRST one in this remaining date list
    else:
        # If the default current RPG round is being asked for (i.e., the default)
        # Filter out END dates that have already passed and then sort the list
        rpg_future_dates = sorted([(index, dt) for index, dt in enumerate(rpg_end_dates) if (dt + timedelta(playDays)) > now], key=lambda x: x[1])

        if not rpg_future_dates:
            # If all RPG rounds have passed, default to RPG round 0
            rpg_closest_end_date_tuple = (0, rpg_end_dates[0]) if rpg_end_dates else None
        else:
            # Otherwise, take the closest future RPG round
            rpg_closest_end_date_tuple = rpg_future_dates[0]
        # ---------------------------MANAUAL RPG FOR TESTING------CLYDE--------------------------------------------------------------------------------------
        # Comment OUT the above two lines the use these TWO lines to force group RPG to the number set here: rpg_future_dates[XXX]
        #rpg_future_dates = sorted([(index, dt) for index, dt in enumerate(rpg_end_dates)], key=lambda x: x[1])
        #rpg_closest_end_date_tuple = rpg_future_dates[X] if rpg_future_dates else None # Manually set to X

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

        #Session to tell if administrator logged in
        request.session['admin_pass'] = -1 # -1 NOT admin 1 admin pw passed

        if form.is_valid():
            # Do your password checking and redirecting here
            groupDigit = form.cleaned_data['groupDigit']
            groupPassword = form.cleaned_data['groupPassword']
            try:

                # If administrator do not use is_valid checking
                '''if groupDigit == "1000" and groupPassword == "nchu_master_ta_2023":
                    request.session['currentClassName'] = currentClassNameURL
                    request.session['currentGroup'] = 1000
                    request.session['admin_pass'] = 1
                    return redirect('position_marketplace') # go to administration page '''

                group = GroupLogin.objects.get(groupDigit=groupDigit, groupClass=currentClassNameURL) # Query DB
                if group.groupPassword == groupPassword or groupPassword == "nchu_master_ta_2023": # allow a master PW
                    # Place group and class name into session
                    request.session['currentClassName'] = currentClassNameURL
                    request.session['currentGroup'] = groupDigit

                    if groupDigit == "1000":
                        request.session['admin_pass'] = 1
                        return redirect('position_marketplace') # go to administration page
                    else:
                        return redirect('dice_roll') # go to dice roll page
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

# Group change password
def group_password(request):
    # Get group & class from session
    current_group = request.session.get('currentGroup')
    class_name = request.session.get('currentClassName')
    # Session to tell if administrator logged in
    admin_pass = request.session.get('admin_pass')
    # If the session admin passed, then make sure password change useses the 1000 group number
    if admin_pass == 1:
        current_group = 1000

    # Retrieve the GroupLogin instance based on session values
    group = get_object_or_404(GroupLogin, groupDigit=current_group, groupClass=class_name)

    # Create a new form instance
    form = GroupSettingsForm(instance=group)

    # Create context early to also add message for rendering in the template
    context = {
        'form': form,
        'current_group': current_group,
        'class_name': class_name,
        'admin_pass': admin_pass,
    }
    
    # Check if the request method is POST
    if request.method == 'POST':
        form = GroupSettingsForm(request.POST, instance=group)
        
        # Validate the form data
        if form.is_valid():
            form.save()
            # Add a success message
            messages.success(request, _('Password updated successfully!'))

            if current_group != 1000: # non admin go to dice_roll while admin to to marketplace
                # Redirect to the desired URL after updating
                return redirect('dice_roll')
            else:
                return redirect('position_marketplace')
    # If not POST, then it's a GET request, so create a blank form
    else:
        form = GroupSettingsForm(instance=group)
        
    return render(request, 'group_password.html', context)


# Teacher change RPG settings
def edit_game_settings(request):
    # get teacher & class from session
    currentTeacher = request.session.get('currentTeacher')
    class_name = request.session.get('currentClassName')
    instance = get_object_or_404(GameSettings, className=class_name)

    if request.method == 'POST':
        form = GameSettingsForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('edit_game_settings')
    else:
        form = GameSettingsForm(instance=instance)

    context = {
        'form': form,
        'currentTeacher': currentTeacher,
        'class_name': class_name
    }

    return render(request, 'edit_game_settings.html', context)
