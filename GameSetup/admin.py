from django.contrib import admin

# Register your models here.

from .models import GroupLogin
@admin.register(GroupLogin)
class GroupLoginAdmin(admin.ModelAdmin):
    list_display = ('display_group','display_password', 'display_class', 'display_teacher', 'display_comment')
    ordering = ('groupTeacher', 'groupClass', 'groupDigit')
    search_fields = ('groupDigit', 'groupClass', 'groupTeacher', 'groupPassword')
    list_filter = ('groupTeacher', 'groupClass')

    def display_group(self, obj):
        return obj.groupDigit
    display_group.short_description = 'Group'

    def display_password(self, obj):
        return obj.groupPassword
    display_password.short_description = 'PW'

    def display_class(self, obj):
        return obj.groupClass
    display_class.short_description = 'Class'

    def display_teacher(self, obj):
        return obj.groupTeacher
    display_teacher.short_description = 'Teacher'

    def display_comment(self, obj):
        return obj.groupComment
    display_comment.short_description = 'Note'

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
    list_display = ('display_class', 'display_rpg', 'display_group', 'display_note', 'display_role', 'display_dice_left', 'display_last_roll', 'display_resistance', 
                    'display_flex', 'display_max', 'display_deliver', 'display_units', 'display_importance', 'display_quality')
    ordering = ('groupClass', 'groupRPG', 'groupDigit')
    search_fields = ('groupDigit', )
    list_filter = ('groupClass', 'groupRPG', 'groupRole', 'groupDiceLeft',)

    def display_class(self, obj):
        return obj.groupClass
    display_class.short_description = 'Class'

    def display_rpg(self, obj):
        return obj.groupRPG
    display_rpg.short_description = 'RPG'

    def display_group(self, obj):
        return obj.groupDigit
    display_group.short_description = 'Group'

    def display_note(self, obj):
        return obj.groupNote
    display_note.short_description = 'Note'
        
    def display_role(self, obj):
        return obj.groupRole
    display_role.short_description = 'Role'

    def display_dice_left(self, obj):
        return obj.groupDiceLeft
    display_dice_left.short_description = 'Left'

    def display_last_roll(self, obj):
        return obj.groupDiceLastRoll
    display_last_roll.short_description = 'Roll'

    def display_resistance(self, obj):
        return obj.groupResistancePrice
    display_resistance.short_description = 'Resist'

    def display_flex(self, obj):
        return obj.groupFlex
    display_flex.short_description = 'Flex'

    def display_max(self, obj):
        return obj.groupMaxPurchase
    display_max.short_description = 'Max'

    def display_deliver(self, obj):
        return obj.groupDelivery
    display_deliver.short_description = 'Deliver'

    def display_units(self, obj):
        return obj.groupUnits
    display_units.short_description = 'Units'

    def display_importance(self, obj):
        return obj.groupUnits
    display_importance.short_description = 'Imp'

    def display_quality(self, obj):
        return obj.groupQuality
    display_quality.short_description = 'Qual'

from position.models import responses
@admin.register(responses)
class responsesAdmin(admin.ModelAdmin):
    list_display = ('display_deal_id', 'display_group', 'display_counterpart','display_buysell', 'display_class', 'display_rpg', 'display_date')
    ordering = ('groupClass', 'groupRPG', 'dealDealID')
    search_fields = ('dealDealID', )
    list_filter = ('groupClass', 'groupRPG', 'dealBuySell',)

    def display_deal_id(self, obj):
        return obj.dealDealID
    display_deal_id.short_description = 'ID'

    def display_group(self, obj):
        return obj.groupDigit
    display_group.short_description = 'Group'

    def display_counterpart(self, obj):
        return obj.dealCounterpart
    display_counterpart.short_description = 'Counterpart'

    def display_buysell(self, obj):
        return obj.dealBuySell
    display_buysell.short_description = 'Role'

    def display_class(self, obj):
        return obj.groupClass
    display_class.short_description = 'Class'

    def display_rpg(self, obj):
        return obj.groupRPG
    display_rpg.short_description = 'RPG'

    def display_date(self, obj):
        return obj.dealDateStamp
    display_date.short_description = 'Time'


from position.models import cancel
@admin.register(cancel)
class cancelAdmin(admin.ModelAdmin):
    list_display = ('display_deal_id', 'display_group', 'display_counterpart', 'display_class', 'display_rpg')
    ordering = ('groupClass', 'groupRPG', 'dealDealID')
    search_fields = ('dealDealID', )
    list_filter = ('groupClass', 'groupRPG',)

    def display_deal_id(self, obj):
        return obj.dealDealID
    display_deal_id.short_description = 'ID'

    def display_group(self, obj):
        return obj.groupDigit
    display_group.short_description = 'Group'

    def display_counterpart(self, obj):
        return obj.dealCounterpart
    display_counterpart.short_description = 'Counterpart'

    def display_class(self, obj):
        return obj.groupClass
    display_class.short_description = 'Class'

    def display_rpg(self, obj):
        return obj.groupRPG
    display_rpg.short_description = 'RPG'

from position.models import gifting
@admin.register(gifting)
class giftingAdmin(admin.ModelAdmin):
    list_display = ('display_time', 'display_receiver', 'display_amount', 'display_group', 'display_class', 'display_rpg')
    ordering = ('groupClass', 'groupRPG', 'giftDateStamp')
    list_filter = ('groupClass', 'groupRPG',)

    def display_time(self, obj):
        return obj.giftDateStamp
    display_time.short_description = 'Time Stamp'

    def display_receiver(self, obj):
        return obj.giftReceiver
    display_receiver.short_description = 'Receiver'

    def display_amount(self, obj):
        return obj.giftAmount
    display_amount.short_description = 'Gift'

    def display_group(self, obj):
        return obj.groupDigit
    display_group.short_description = 'Group'

    def display_class(self, obj):
        return obj.groupClass
    display_class.short_description = 'Class'

    def display_rpg(self, obj):
        return obj.groupRPG
    display_rpg.short_description = 'RPG'

from position.models import messaging
@admin.register(messaging)
class messagingAdmin(admin.ModelAdmin):
    list_display = ('messageDateStamp', 'messageSubject', 'messageReceiver', 'display_group', 'display_class', 'display_rpg')
    ordering = ('groupClass', 'groupRPG', 'messageDateStamp')
    list_filter = ('groupClass', 'groupRPG',)

    def display_class(self, obj):
        return obj.groupClass
    display_class.short_description = 'Class'

    def display_rpg(self, obj):
        return obj.groupRPG
    display_rpg.short_description = 'RPG'

    def display_group(self, obj):
        return obj.groupDigit
    display_group.short_description = 'Group'


