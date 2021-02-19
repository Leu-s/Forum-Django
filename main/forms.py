from django import forms
from .models import AdvancedUser


class UserPersonalInformationForm(forms.ModelForm):
    class Meta:
        model = AdvancedUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'village',
            'date_of_birth',
        )
