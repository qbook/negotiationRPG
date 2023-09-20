from django.db import models
from django.utils import timezone
from decimal import Decimal

# Create your models here.

class responses(models.Model):
    #Group+Class+RPG is unique Only insert once
    groupDigit = models.IntegerField(blank=True, null=True, default=0)
    groupClass = models.CharField(blank=True, null=True, max_length=200)
    groupRPG = models.IntegerField(blank=True, null=True, default=0)

    #These values get updated when user submits a deal
    #datestamp is for research, actual time of submission
    dealDateStamp = models.DateTimeField(default=timezone.now)

    #the deal ID is based on a timestamp, but it is just a identifier to pass to counterparties
    dealDealID = models.IntegerField(blank=True, null=True, default=0)
    dealCounterpart = models.IntegerField(blank=True, null=True, default=0)    
    #Buy/sell is 1/-1
    dealBuySell = models.IntegerField(blank=True, null=True, default=0)
    dealUnits = models.IntegerField(blank=True, null=True, default=0)
    dealPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=Decimal('0.00'))
    dealQuality = models.IntegerField(blank=True, null=True, default=0)
    dealDelivery = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return str(self.groupDigit)
    class Meta:
        verbose_name = 'Deal Responses'
        verbose_name_plural = 'Deal Responses'

class cancel(models.Model):
    #Group+Class+RPG is unique Only insert once
    groupDigit = models.IntegerField(blank=True, null=True, default=0)
    groupClass = models.CharField(blank=True, null=True, max_length=200)
    groupRPG = models.IntegerField(blank=True, null=True, default=0)

    #These values get updated when user submits a cancel
    #datestamp is for research, actual time of submission
    dealDateStamp = models.DateTimeField(default=timezone.now)

    #the deal ID is based on a timestamp, but it is just a identifier to pass to counterparties
    dealDealID = models.IntegerField(blank=True, null=True, default=0)
    dealCounterpart = models.IntegerField(blank=True, null=True, default=0)    


    def __str__(self):
        return str(self.groupDigit)
    class Meta:
        verbose_name = 'Deal Cancel'
        verbose_name_plural = 'Deal Cancel'

class gifting(models.Model):
    #Group+Class+RPG is unique Only insert once
    groupDigit = models.IntegerField(blank=True, null=True, default=0)
    groupClass = models.CharField(blank=True, null=True, max_length=200)
    groupRPG = models.IntegerField(blank=True, null=True, default=0)

    #These values get updated when user submits gifting Flex Points
    #datestamp is for research, actual time of submission
    giftDateStamp = models.DateTimeField(default=timezone.now)

    #the message needs sender=groupDigit, receiver, subject, and content
    giftReceiver = models.IntegerField(blank=True, null=True, default=0)
    giftAmount = models.IntegerField(blank=True, null=True, default=0)
    giftMessage = models.TextField(blank=True, null=True, max_length=200)

    def __str__(self):
        return str(self.groupDigit)
    class Meta:
        verbose_name = 'Flex Point Gift'
        verbose_name_plural = 'Flex Point Gifts'

class messaging(models.Model):
    #Group+Class+RPG is unique Only insert once
    groupDigit = models.IntegerField(blank=True, null=True, default=0)
    groupClass = models.CharField(blank=True, null=True, max_length=200)
    groupRPG = models.IntegerField(blank=True, null=True, default=0)

    #These values get updated when user submits a message
    #datestamp is for research, actual time of submission
    messageDateStamp = models.DateTimeField(default=timezone.now)

    #the message needs sender=groupDigit, receiver, subject, and content
    messageReceiver = models.IntegerField(blank=True, null=True, default=0)
    messageSubject = models.CharField(blank=True, null=True, max_length=200)
    messageContent = models.TextField(blank=True, null=True, default="")

    def __str__(self):
        return str(self.groupDigit)
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


