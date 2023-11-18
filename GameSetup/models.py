from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.utils.safestring import mark_safe

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

# Helper function to provide default datetime with added hours/days
def default_time_plus(days=0, hours=0):
    return timezone.now() + timedelta(days=days, hours=hours)


class GameSettings(models.Model):
    teacher = models.CharField(max_length=200, help_text = 'Prof. Clyde Warden', default='Prof. Clyde Warden')
    className = models.CharField(max_length=200, help_text='NTU_Negotiation_2023_2', default='NTU_Negotiation_2023_2')
    created = models.DateTimeField(auto_now_add=True, null=True)
    lastUpdate = models.DateField(auto_now_add=True, null=True)
    numberOfGroups = models.IntegerField(blank=True, default=50)
    numberOfMembers = models.IntegerField(blank=True, default=3)
    diceHigh = models.IntegerField(blank=True, help_text='sugested min=10 max=28; All dice=48', default='28')
    diceLow = models.IntegerField(blank=True, help_text='10', default='10')
    playDays = models.IntegerField(blank=True, help_text='5', default='5')
    teacherNotes = models.TextField(blank=True, default='Your notes here', help_text='Only seen by instructor')

    userGuide = models.CharField(blank=False, max_length=1000, help_text='User Guide', default=mark_safe('<a href="https://drive.google.com/open?id=1erZQh-xTOjtuajoRr4pIa030z3d2729d" target="_blank"Pet Feeder</a>'))
    eBook = models.CharField(blank=False, max_length=1000, help_text='Class eBook', default=mark_safe('<a href="https://drive.google.com/open?id=1erZQh-xTOjtuajoRr4pIa030z3d2729d" target="_blank"Pet Feeder</a>'))
    classSlides = models.CharField(blank=False, max_length=1000, help_text='Class Slides', default=mark_safe('<a href="https://drive.google.com/open?id=1erZQh-xTOjtuajoRr4pIa030z3d2729d" target="_blank">Pet Feeder</a>'))
    videoLectures = models.CharField(blank=False, max_length=1000, help_text='Video Lectures', default=mark_safe('<a href="https://drive.google.com/open?id=1erZQh-xTOjtuajoRr4pIa030z3d2729d" target="_blank">Pet Feeder</a>'))

    round0Start = models.DateTimeField(default=default_time_plus(days=0,hours=1))
    round0ProductName = models.CharField(blank=False, max_length=1000, help_text='Pet Feeder', default=mark_safe('<a href="https://drive.google.com/open?id=1erZQh-xTOjtuajoRr4pIa030z3d2729d" target="_blank">Pet Feeder</a>'))
    round0ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=False, help_text='320', default='320')
    round0ProductUnits = models.IntegerField(blank=False, help_text='6000', default='6000')
    round0ProductCurrency = models.CharField(blank=False, max_length=50, help_text='NTD', default='NTD')
    round0End = models.DateTimeField(default=default_time_plus(days=0,hours=5))
    
    round1Start = models.DateTimeField(default=default_time_plus(days=7,hours=0))
    round1ProductName = models.CharField(blank=False, max_length=1000, help_text='Baby Car Seat', default=mark_safe('<a href="https://drive.google.com/open?id=11sKz1NUVK_HOIUZYTRbtLEvxCYmSKlsi" target="_blank">Baby Car Seat</a>'))
    round1ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='1450', default='1450')
    round1ProductUnits = models.IntegerField(blank=True, help_text='1000', default='1000')
    round1ProductCurrency = models.CharField(blank=True, max_length=50, help_text='NTD', default='NTD')
    round1End = models.DateTimeField(default=default_time_plus(days=7,hours=5))

    round2Start = models.DateTimeField(default=default_time_plus(days=14,hours=0))
    round2ProductName = models.CharField(blank=False, max_length=1000, help_text='Winter Ear Muffs', default=mark_safe('<a href="https://drive.google.com/open?id=1aM1oXLHkLi2t1Vj31dEQuOpkVTfOSwHN" target="_blank">Winter Ear Muffs</a>'))
    round2ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='250', default='250')
    round2ProductUnits = models.IntegerField(blank=True, help_text='10000', default='10000')
    round2ProductCurrency = models.CharField(blank=True, max_length=50, help_text='NTD', default='NTD')
    round2End = models.DateTimeField(default=default_time_plus(days=14,hours=5))

    round3Start = models.DateTimeField(default=default_time_plus(days=21,hours=0))
    round3ProductName = models.CharField(blank=False, max_length=1000, help_text='Foldable Pet Carrier', default=mark_safe('<a href="https://drive.google.com/open?id=1wdj2VZ2qnsZp5ahswQrr7GX5--xtgFTJ" target="_blank">Foldable Pet Carrier</a>'))
    round3ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='7500', default='7500')
    round3ProductUnits = models.IntegerField(blank=True, help_text='1200', default='1200')
    round3ProductCurrency = models.CharField(blank=True, max_length=50, help_text='NTD', default='NTD')
    round3End = models.DateTimeField(default=default_time_plus(days=21,hours=5))

    round4Start = models.DateTimeField(default=default_time_plus(days=28,hours=0))
    round4ProductName = models.CharField(blank=False, max_length=1000, help_text='LED Christmas Tree', default=mark_safe('<a href="https://drive.google.com/open?id=15YnZ__lkJNBIZpJ6TtJEAJ6CNEODtVKC" target="_blank">LED Christmas Tree</a>'))
    round4ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='1200', default='1200')
    round4ProductUnits = models.IntegerField(blank=True, help_text='6500', default='6500')
    round4ProductCurrency = models.CharField(blank=True, max_length=50, help_text='USD', default='USD')
    round4End = models.DateTimeField(default=default_time_plus(days=28,hours=5))

    round5Start = models.DateTimeField(default=default_time_plus(days=35,hours=0))
    round5ProductName = models.CharField(blank=False, max_length=1000, help_text='Abdominal Exercise Equipment', default=mark_safe('<a href="https://drive.google.com/open?id=1utnjF1_hnfFqPKYIOMoBKeyHfdbpHCGu" target="_blank">Abdominal Exercise Equipment</a>'))
    round5ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='6.5', default='6.5')
    round5ProductUnits = models.IntegerField(blank=True, help_text='11000', default='11000')
    round5ProductCurrency = models.CharField(blank=True, max_length=50, help_text='USD', default='USD')
    round5End = models.DateTimeField(default=default_time_plus(days=35,hours=5))

    round6Start = models.DateTimeField(default=default_time_plus(days=42,hours=0))
    round6ProductName = models.CharField(blank=False, max_length=1000, help_text='Color LED Calendar', default=mark_safe('<a href="https://drive.google.com/open?id=1NU3l9HVZEXi5YR2Dmx7hqyqtJi6LBcHu" target="_blank">Color LED Calendar</a>'))
    round6ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='1600', default='1600')
    round6ProductUnits = models.IntegerField(blank=True, help_text='1200', default='1200')
    round6ProductCurrency = models.CharField(blank=True, max_length=50, help_text='NTD', default='NTD')
    round6End = models.DateTimeField(default=default_time_plus(days=42,hours=5))

    round7Start = models.DateTimeField(default=default_time_plus(days=49,hours=0))
    round7ProductName = models.CharField(blank=False, max_length=1000, help_text='The Lil Hombre Two-in-one', default=mark_safe('<a href="https://drive.google.com/open?id=1sWk_oR9vXUPTjO34Ijk4CZH0MrHiffuf" target="_blank">The Lil Hombre Two-in-one</a>'))
    round7ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='3060', default='3060')
    round7ProductUnits = models.IntegerField(blank=True, help_text='1800', default='1800')
    round7ProductCurrency = models.CharField(blank=True, max_length=50, help_text='USD', default='USD')
    round7End = models.DateTimeField(default=default_time_plus(days=49,hours=5))

    round8Start = models.DateTimeField(default=default_time_plus(days=56,hours=0))
    round8ProductName = models.CharField(blank=False, max_length=1000, help_text='Kitchen Make Believe', default=mark_safe('<a href="https://drive.google.com/open?id=1qYi-CgHhDHDb5zrscqxtB6jNRqSl1bxW" target="_blank">Kitchen Make Believe</a>'))
    round8ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='10.5', default='10.5')
    round8ProductUnits = models.IntegerField(blank=True, help_text='10850', default='10850')
    round8ProductCurrency = models.CharField(blank=True, max_length=50, help_text='USD', default='USD')
    round8End = models.DateTimeField(default=default_time_plus(days=56,hours=5))

    round9Start = models.DateTimeField(default=default_time_plus(days=63,hours=0))
    round9ProductName = models.CharField(blank=False, max_length=1000, help_text='Sports Carry Duffle Bag', default=mark_safe('<a href="https://drive.google.com/open?id=1Iv_w-HHZyn6-rFt77KT6peO2ZxzZ0rUT" target="_blank">Sports Carry Duffle Bag</a>'))
    round9ProductPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, help_text='1450', default='1450')
    round9ProductUnits = models.IntegerField(blank=True, help_text='3800', default='3800')
    round9ProductCurrency = models.CharField(blank=True, max_length=50, help_text='USD', default='USD')
    round9End = models.DateTimeField(default=default_time_plus(days=63,hours=5))
 
    class Meta:
        verbose_name = 'Game Settings'
        verbose_name_plural = 'Game Settings'

    def __str__(self):     
        return self.className
 