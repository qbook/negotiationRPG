# forms.py
from django import forms
from .models import GroupLogin

class GroupDigitForm(forms.Form):
    group_digit = forms.ChoiceField(choices=[])
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unique_group_digits = GroupLogin.objects.values_list('groupDigit', flat=True).distinct()
        self.fields['group_digit'].choices = [(digit, digit) for digit in unique_group_digits]



