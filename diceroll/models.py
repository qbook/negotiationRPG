from django.db import models

# Create your models here.

class GroupCharacterSheet(models.Model):
    #Group+Class+RPG is unique Only insert once
    groupDigit = models.IntegerField(blank=True, null=True, default=0)
    groupClass = models.CharField(blank=True, null=True, max_length=200)
    groupRPG = models.IntegerField(blank=True, null=True, default=0)
    #Update rolls to DB each time in order to prevent too many rolls
    groupDiceLeft = models.IntegerField(blank=True, null=True, default=5)
    #Save the last roll value to appear next time page is opened
    groupDiceLastRoll = models.IntegerField(blank=True, null=True, default=0)
    #These values get updated when user locks in scores to play
    groupResistancePrice = models.IntegerField(blank=True, null=True, default=0)
    groupFlex = models.IntegerField(blank=True, null=True, default=0)
    groupMaxPurchase = models.IntegerField(blank=True, null=True, default=0)    
    groupDelivery = models.IntegerField(blank=True, null=True, default=0)
    groupUnits = models.IntegerField(blank=True, null=True, default=0)
    groupImportance = models.IntegerField(blank=True, null=True, default=0)
    groupQuality = models.IntegerField(blank=True, null=True, default=0)
    groupRole = models.IntegerField(blank=True, null=True, default=0)
    # Research data collection
    groupFirstRoll = models.DateTimeField(blank=True, null=True)
    groupPlayNow = models.DateTimeField(blank=True, null=True)
    groupPageRefresh = models.IntegerField(blank=True, null=True, default=0)
    # Note (not currently used on student side)
    groupNote = models.CharField(max_length=200, default='Note.')

    def __str__(self):
        return str(self.groupDigit)
    class Meta:
        verbose_name = 'Group Character Sheet'
        verbose_name_plural = 'Group Character Sheet'


