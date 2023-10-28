# forms.py
from django import forms
from .models import GroupLogin
from .models import GameSettings

class GroupDigitForm(forms.Form):
    group_digit = forms.ChoiceField(choices=[])
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        unique_group_digits = GroupLogin.objects.values_list('groupDigit', flat=True).distinct()
        self.fields['group_digit'].choices = [(digit, digit) for digit in unique_group_digits]

class GroupLoginForm(forms.Form):
    groupPassword = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'style': 'max-width: 100%; width: 300px;'}))
    groupDigit = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super(GroupLoginForm, self).__init__(*args, **kwargs)
        self.fields['groupDigit'].choices = [(group.groupDigit, group.groupDigit) for group in GroupLogin.objects.all()]

# Group settings
class GroupSettingsForm(forms.ModelForm):
    class Meta:
        model = GroupLogin
        fields = ['groupPassword']
        labels = {
            'groupPassword': 'New Password:',
        }

# For the administration changes of RPG game settings
class GameSettingsForm(forms.ModelForm): 
    class Meta:
        model = GameSettings
        exclude = ['teacher', 'className', 'created']
