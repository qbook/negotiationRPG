from django.contrib import admin

# Register your models here.

from .models import GroupLogin
@admin.register(GroupLogin)
class GroupLoginAdmin(admin.ModelAdmin):
    list_display = ('groupDigit', 'groupTeacher', 'groupClass', 'groupPassword', 'groupComment')

from .models import GameTest
@admin.register(GameTest)
class GameTestAdmin(admin.ModelAdmin):
    list_display = ('gameGroupComment', 'gameGroupNumber', 'gameGroupDigit')

from .models import GameSettings
@admin.register(GameSettings)
class GameSettingsAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'className', 'diceHigh', 'diceLow')
    list_filter = ('teacher', 'className')
    search_fields = ('className', 'teacher')
    ordering = ('className', 'teacher')

from diceroll.models import GroupCharacterSheet
@admin.register(GroupCharacterSheet)
class GroupCharacterSheetAdmin(admin.ModelAdmin):
    list_display = ('groupClass', 'groupRPG', 'groupDigit', 'groupRole', 'groupDiceLeft')
    ordering = ('groupClass', 'groupRPG', 'groupDigit')

from position.models import responses
@admin.register(responses)
class responsesAdmin(admin.ModelAdmin):
    list_display = ('dealDealID', 'groupDigit', 'dealBuySell', 'groupClass', 'groupRPG')
    ordering = ('groupClass', 'groupRPG', 'dealDealID')

from position.models import cancel
@admin.register(cancel)
class cancelAdmin(admin.ModelAdmin):
    list_display = ('dealDealID', 'groupDigit', 'groupClass', 'groupRPG')
    ordering = ('groupClass', 'groupRPG', 'dealDealID')

from position.models import gifting
@admin.register(gifting)
class giftingAdmin(admin.ModelAdmin):
    list_display = ('giftDateStamp', 'giftReceiver', 'giftAmount', 'groupDigit', 'groupClass', 'groupRPG')
    ordering = ('groupClass', 'groupRPG', 'giftDateStamp')

from position.models import messaging
@admin.register(messaging)
class messagingAdmin(admin.ModelAdmin):
    list_display = ('messageDateStamp', 'messageSubject', 'messageReceiver', 'groupDigit', 'groupClass', 'groupRPG')
    ordering = ('groupClass', 'groupRPG', 'messageDateStamp')




