# forms.py
from django import forms
from decimal import Decimal

class DealForm(forms.Form):
    counterparty = forms.IntegerField(label="Counterpart:")
    units = forms.IntegerField(label="Units:")
    price = forms.DecimalField(max_digits=10, decimal_places=2, initial=Decimal('0.00'), label="Price:")
    QUALITY_CHOICES = [
        (0, '-----'),
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    quality = forms.ChoiceField(choices=QUALITY_CHOICES, label="Quality:")
    DELIVERY_CHOICES = [
        (0, '-----'),
        (1, 'Slow'),
        (2, 'Average'),
        (3, 'Fast'),
    ]
    delivery = forms.ChoiceField(choices=DELIVERY_CHOICES, label="Delivery:")
    dealID = forms.IntegerField(label="Deal ID:")

class CancelForm(forms.Form):
    dealIDCancel = forms.IntegerField(label="Deal ID:")
    counterpartyCancel = forms.IntegerField(label="Counterpart:")

class GiftingForm(forms.Form):
    giftReceiver = forms.IntegerField(label="Receiver:")
    giftAmount = forms.IntegerField(label="Amount:")
    giftMessage = forms.CharField(label="Message:")

class MessagingForm(forms.Form):
    messageReceiver = forms.IntegerField(label="Receiver:")
    messageSubject = forms.CharField(label="Subject:")
    messageContent = forms.CharField(label="Message:")
