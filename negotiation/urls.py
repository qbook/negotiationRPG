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
from django.urls import path
from GameSetup import views as gameSetupViews
from diceroll import views as diceRollViews
from position import views as positionViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', gameSetupViews.home, name='home'),
    path('setup/', gameSetupViews.setup, name='setup'),
    path('save_note/', gameSetupViews.save_note, name='save_note'),

    path('choose_group/', gameSetupViews.choose_group, name='choose_group'),

    path('login/', gameSetupViews.login, name='login'),
    path('about/', gameSetupViews.about, name='about'),
    path('dice_roll/', diceRollViews.group_character, name='dice_roll'),
    path('generate_random_number/', diceRollViews.generate_random_number, name='generate_random_number'),
    path('roll_dice/', diceRollViews.roll_dice, name='roll_dice'),
    path('update_attributes/', diceRollViews.update_attributes, name='update_attributes'),

    path('position_buyer_seller/', positionViews.position_buyer_seller, name='position_buyer_seller'),

    path('position_marketplace/', positionViews.position_marketplace, name='position_marketplace'),

    path('save_deal/', positionViews.save_deal, name='save_deal'),
    path('cancel_deal/', positionViews.cancel_deal, name='cancel_deal'),

    path('gift_flex/', positionViews.gift_flex, name='gift_flex'),
    path('send_message/', positionViews.send_message, name='send_message'),

]






