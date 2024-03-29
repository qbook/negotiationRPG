"""
URL configuration for negotiation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.views.i18n import set_language
from GameSetup import views as gameSetupViews
from diceroll import views as diceRollViews
from position import views as positionViews
from survey import views as surveyViews


urlpatterns = [

    path('survey/start/', surveyViews.start_survey, name='start_survey'),
    path('survey/<int:code_order>/', surveyViews.survey_view, name='survey_view'),
    path('survey/submit/<int:code_order>/', surveyViews.submit_survey, name='submit_survey'),
    path('survey/complete/', surveyViews.survey_complete, name='survey_complete'),

    path('set-language/', set_language, name='set_language'),
    path('admin/', admin.site.urls),
    path('', gameSetupViews.home, name='home'),
    path('setup/', gameSetupViews.setup, name='setup'),
    path('save_note/', gameSetupViews.save_note, name='save_note'),
    path('edit_game_settings/', gameSetupViews.edit_game_settings, name='edit_game_settings'),
    path('admin_password/', gameSetupViews.group_password, name='group_password'),
    # Import CSV class/group membership
    path('upload_csv/', gameSetupViews.upload_csv, name='upload_csv'),
    # View survey results in tabular layout
    path('survey_results/', surveyViews.survey_results, name='survey_results'),

    path('choose_group/', gameSetupViews.choose_group, name='choose_group'),

    path('login/', gameSetupViews.login, name='login'),
    path('about/', gameSetupViews.about, name='about'),
    path('dice_roll/', diceRollViews.group_character, name='dice_roll'),
    path('generate_random_number/', diceRollViews.generate_random_number, name='generate_random_number'),
    path('roll_dice/', diceRollViews.roll_dice, name='roll_dice'),
    path('update_attributes/', diceRollViews.update_attributes, name='update_attributes'),

    path('group_password/', gameSetupViews.group_password, name='group_password'),
    #path('update_group_password/<int:group_id>/', gameSetupViews.update_group_password, name='update_group_password'),

    # Current position status readouts
    path('position_buyer_seller/', positionViews.position_buyer_seller, name='position_buyer_seller'),
    path('position_marketplace/', positionViews.position_marketplace, name='position_marketplace'),
    
    # Manual RPG round selection for current position status readouts
    path('position_marketplace_manual/', positionViews.position_marketplace_manual, name='position_marketplace_manual'),
    path('position_buyer_seller/', positionViews.position_buyer_seller, name='position_buyer_seller_manual'),

    path('save_deal/', positionViews.save_deal, name='save_deal'),
    path('cancel_deal/', positionViews.cancel_deal, name='cancel_deal'),

    path('gift_flex/', positionViews.gift_flex, name='gift_flex'),
    path('send_message/', positionViews.send_message, name='send_message'),

    # Admin page actions
    path('remove_deal/<int:deal_id>/', positionViews.remove_deal, name='remove_deal'),
    path('position_result', positionViews.position_result, name='position_result'),
    path('position_result_manual', positionViews.position_result_manual, name='position_result_manual'),

]

urlpatterns += i18n_patterns(
    # ... patterns for which you want to enable language changing ...
    path('set-language/', include('django.conf.urls.i18n')),
)
