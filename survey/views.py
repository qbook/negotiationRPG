from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from .models import SurveySection, SurveyQuestion, UserResponse
from GameSetup.models import GameSettings
import random
# from django.contrib.auth.models import User
from django.utils import timezone

# Create your views here.
from django.shortcuts import render, redirect
from .models import SurveySection, UserResponse
import random

def start_survey(request):
    # -------FOR TESTING CLYDE--------------------------------------------------------
    #student_id = '123456'
    #request.session['student_id'] = student_id
    # -------END TESTING CLYDE--------------------------------------------------------

    # Check if 'student_id' is already set in the session
    if 'student_id' in request.session:
        # Assign from session to local variable
        student_id = request.session['student_id']
    else:
        # Get 'student_id' from URL parameters
        student_id = request.GET.get('student_id')
        if student_id:
            # Set 'student_id' in the session and local variable
            request.session['student_id'] = student_id

    if not student_id:
        # Redirect to a page where student_id can be set or retrieved
        return redirect('position_buyer_seller') #-------------CLYDE set this to the choose user maybe------

    # Get a list of section codes that the student has not completed
    completed_section_codes = UserResponse.objects.filter(
        student_id=student_id
    ).values_list('section_code', flat=True).distinct()
    completed_section_codes = [int(code) for code in completed_section_codes] # Convert completed_section_codes to integers
    all_section_codes = SurveySection.objects.values_list('code_order', flat=True)
    uncompleted_section_codes = list(set(all_section_codes) - set(completed_section_codes))
    random.shuffle(uncompleted_section_codes) # Randomize the order of the uncompleted sections
    remaining_sections_count = len(uncompleted_section_codes)

    if not uncompleted_section_codes:
        return redirect('survey_complete')

    random_code_order = random.choice(uncompleted_section_codes)

    # Redirect to the survey view for the random section
    # Pass the remaining_sections_count as a part of the session
    request.session['remaining_sections_count'] = remaining_sections_count
    return redirect('survey_view', code_order=random_code_order)


def survey_view(request, code_order):
    # Retrieve remaining_sections_count from the session
    remaining_sections_count = request.session.get('remaining_sections_count', 0)

    section = get_object_or_404(SurveySection, code_order=code_order)
    questions = list(section.questions.all())  # Convert QuerySet to a list for shuffling
    random.shuffle(questions)  # Randomize the order of questions

    currentClassName = request.session.get('currentClassName')
    student_id = request.session.get('student_id')

    context = {
        'section': section,
        'questions': questions,
        'remaining_sections_count': remaining_sections_count,
        'student_id': student_id,
        'currentClassName': currentClassName,
    }
    return render(request, 'survey.html', context)

def submit_survey(request, code_order):
    if request.method == 'POST':
        student_id = request.session.get('student_id')

        # Get the corresponding section based on code_order
        section = get_object_or_404(SurveySection, code_order=code_order)
        
        # Iterate over the questions and save responses
        for question in section.questions.all():
            response_key = f'question_{question.id}'
            if response_key in request.POST:
                response_value = request.POST[response_key]
                UserResponse.objects.update_or_create(
                    student_id=student_id,
                    section_code=section.code_order,  # Assuming 'code_order' is the field in SurveySection
                    question_number=question.question_number,  # Use the new field
                    defaults={
                        'response': response_value,
                        'dateStamp': timezone.now()  # Set the current time for dateStamp
                    }
                )
            else:
                messages.error(request, "Missing response for some questions.")
                return redirect('survey_view', code_order=code_order)

        # After saving responses, redirect back to start_survey
        return redirect('start_survey')

    # Redirect back to the survey section if it's not a POST request
    return redirect('survey_view', code_order=code_order)

def survey_complete(request):
    student_id = request.session.get('student_id')

    request.session.pop('student_id', None) # Remove 'student_id' from the session as survey is complete
    
    currentClassName = request.session.get('currentClassName')

    # Query the current class to get the survey gift link
    surveyReward_queryset = GameSettings.objects.filter(
        className=currentClassName,
     ).values('surveyReward')
    # Since you're expecting one result, you can use first()
    surveyReward = surveyReward_queryset.first()['surveyReward'] if surveyReward_queryset.exists() else None

    context = {
        'student_id': student_id,
        'surveyReward': surveyReward,
    }
    return render(request, 'survey_complete.html', context)

