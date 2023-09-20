from django.db import models
from django.utils import timezone

# Create your models here.

class GroupLogin(models.Model):
    groupComment = models.CharField(max_length=100)
    groupPassword = models.CharField(max_length=20)
    groupDigit = models.IntegerField(blank=True, null=True, default=0)
    groupTeacher = models.CharField(max_length=200)
    groupClass = models.CharField(blank=True, null=True, max_length=200)
    def __str__(self):
        return str(self.groupDigit)
    class Meta:
        verbose_name = 'Group Login'
        verbose_name_plural = 'Group Login'

class GameTest(models.Model):
    gameGroupComment = models.CharField(max_length=200)
    gameGroupNumber = models.CharField(max_length=200)
    gameGroupDigit = models.IntegerField(blank=True, default=0)
    def __str__(self):
        return self.gameGroupNumber
    class Meta:
        verbose_name = 'Game Test Clyde'
        verbose_name_plural = 'Game Test Clyde'

class GameSettings(models.Model):
    teacher = models.CharField(max_length=200, help_text = 'Prof. Clyde Warden', default='Prof. Clyde Warden')
    className = models.CharField(max_length=200, help_text='NTU_Negotiation_2023_2', default='NTU_Negotiation_2023_2')
    created = models.DateField(auto_now_add=True, null=True)
    lastUpdate = models.DateField(blank=True, null=True)
    numberOfGroups = models.IntegerField(blank=True, default='50')
    numberOfMembers = models.IntegerField(blank=True, default='3')
    diceHigh = models.IntegerField(blank=True, help_text='sugested min=10 max=28; All dice=48', default='28')
    diceLow = models.IntegerField(blank=True, help_text='10', default='10')
    playDays = models.IntegerField(blank=True, help_text='5', default='5')
    teacherNotes = models.TextField(blank=True, default='Your notes here', help_text='Only seen by instructor')

    round0Start = models.DateTimeField(blank=True, null=True)
    round0ProductName = models.CharField(blank=True, max_length=200, help_text='Pet Feeder', default='Pet Feeder')
    round0ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='320', default='320')
    round0ProductUnits = models.IntegerField(blank=True, help_text='6000', default='6000')
    round0ProductCurrency = models.CharField(blank=True, max_length=50, help_text='NTD', default='NTD')
    round0End = models.DateTimeField(blank=True, null=True)

    round1Start = models.DateTimeField(blank=True, null=True)
    round1ProductName = models.CharField(blank=True, max_length=200, help_text='Baby Car Seat', default='Baby Car Seat')
    round1ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='1450', default='1450')
    round1ProductUnits = models.IntegerField(blank=True, help_text='1000', default='1000')
    round1ProductCurrency = models.CharField(blank=True, max_length=50, help_text='NTD', default='NTD')
    round1End = models.DateTimeField(blank=True, null=True)

    round2Start = models.DateTimeField(blank=True, null=True)
    round2ProductName = models.CharField(blank=True, max_length=200, help_text='Winter Ear Muffs', default='Winter Ear Muffs')
    round2ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='250', default='250')
    round2ProductUnits = models.IntegerField(blank=True, help_text='10000', default='10000')
    round2ProductCurrency = models.CharField(blank=True, max_length=50, help_text='NTD', default='NTD')
    round2End = models.DateTimeField(blank=True, null=True)

    round3Start = models.DateTimeField(blank=True, null=True)
    round3ProductName = models.CharField(blank=True, max_length=200, help_text='Foldable Pet Carrier', default='Foldable Pet Carrier')
    round3ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='7500', default='7500')
    round3ProductUnits = models.IntegerField(blank=True, help_text='1200', default='1200')
    round3ProductCurrency = models.CharField(blank=True, max_length=50, help_text='NTD', default='NTD')
    round3End = models.DateTimeField(blank=True, null=True)

    round4Start = models.DateTimeField(blank=True, null=True)
    round4ProductName = models.CharField(blank=True, max_length=200, help_text='LED Christmas Tree', default='LED Christmas Tree')
    round4ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='1200', default='1200')
    round4ProductUnits = models.IntegerField(blank=True, help_text='6500', default='6500')
    round4ProductCurrency = models.CharField(blank=True, max_length=50, help_text='USD', default='USD')
    round4End = models.DateTimeField(blank=True, null=True)

    round5Start = models.DateTimeField(blank=True, null=True)
    round5ProductName = models.CharField(blank=True, max_length=200, help_text='Abdominal Exercise Equipment', default='Abdominal Exercise Equipment')
    round5ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='6.5', default='6.5')
    round5ProductUnits = models.IntegerField(blank=True, help_text='11000', default='11000')
    round5ProductCurrency = models.CharField(blank=True, max_length=50, help_text='USD', default='USD')
    round5End = models.DateTimeField(blank=True, null=True)

    round6Start = models.DateTimeField(blank=True, null=True)
    round6ProductName = models.CharField(blank=True, max_length=200, help_text='Color LED Calendar', default='Color LED Calendar')
    round6ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='1600', default='1600')
    round6ProductUnits = models.IntegerField(blank=True, help_text='1200', default='1200')
    round6ProductCurrency = models.CharField(blank=True, max_length=50, help_text='NTD', default='NTD')
    round6End = models.DateTimeField(blank=True, null=True)

    round7Start = models.DateTimeField(blank=True, null=True)
    round7ProductName = models.CharField(blank=True, max_length=200, help_text='The Lil Hombre Two-in-one', default='The Lil Hombre Two-in-one')
    round7ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='3060', default='3060')
    round7ProductUnits = models.IntegerField(blank=True, help_text='1800', default='1800')
    round7ProductCurrency = models.CharField(blank=True, max_length=50, help_text='USD', default='USD')
    round7End = models.DateTimeField(blank=True, null=True)

    round8Start = models.DateTimeField(blank=True, null=True)
    round8ProductName = models.CharField(blank=True, max_length=200, help_text='Kitchen Make Believe', default='Kitchen Make Believe')
    round8ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='10.5', default='10.5')
    round8ProductUnits = models.IntegerField(blank=True, help_text='10850', default='10850')
    round8ProductCurrency = models.CharField(blank=True, max_length=50, help_text='USD', default='USD')
    round8End = models.DateTimeField(blank=True, null=True)

    round9Start = models.DateTimeField(blank=True, null=True)
    round9ProductName = models.CharField(blank=True, max_length=200, help_text='Sports Carry Duffle Bag', default='Sports Carry Duffle Bag')
    round9ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='1450', default='1450')
    round9ProductUnits = models.IntegerField(blank=True, help_text='3800', default='3800')
    round9ProductCurrency = models.CharField(blank=True, max_length=50, help_text='USD', default='USD')
    round9End = models.DateTimeField(blank=True, null=True)
 
    class Meta:
        verbose_name = 'Game Settings'
        verbose_name_plural = 'Game Settings'

    def __str__(self):     
        return self.className
 