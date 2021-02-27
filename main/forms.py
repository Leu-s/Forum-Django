from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .utilities import available_birth_years
from .models import AdvancedUser
from .models import user_registrated


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        label='Email адреса',
        help_text='Приклад: example@abc.com'
    )
    password1 = forms.CharField(
        min_length=8,
        label='Пароль',
        required=True,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Повторіть пароль',
        required=True,
        widget=forms.PasswordInput,
        help_text='Введить свій пароль ще раз для перевірки'
    )

    def add_error(self, field, error):
        if field is not None:
            print(f'Error on field {field}: {error}')
        else:
            print(f'Error on form: {error}')
        super().add_error(field, error)

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 \
                and password1 != password2:
            raise ValidationError(
                'Паролі не співпали',
                code='password_mismatch'
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        password = self.cleaned_data['password1']
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password1', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_activated = False
        if commit:
            user.save()
        user_registrated.send(UserRegistrationForm, instance=user)  # Send activation email
        return user

    class Meta:
        model = AdvancedUser
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


# class UserPersonalInformationForm(forms.ModelForm):
#     class Meta:
#         model = AdvancedUser
#         fields = (
#             'first_name',
#             'last_name',
#             'email',
#             'phone_number',
#             'village',
#             'date_of_birth',
#             'user_image',
#             'about_me'
#         )
#
#         widgets = {
#             'date_of_birth': forms.SelectDateWidget(years=available_birth_years()),
#         }


class FirstPersonalInformationForm(forms.ModelForm):
    class Meta:
        model = AdvancedUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
        )


class SecondPersonalInformationForm(forms.ModelForm):

    def add_error(self, field, error):
        if field is not None:
            print(f'Error on field {field}: {error}')
        else:
            print(f'Error on form: {error}')
        super().add_error(field, error)

    class Meta:
        model = AdvancedUser
        fields = (
            'user_image',
            'village',
            'date_of_birth',
            'about_me',
        )

        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=available_birth_years()),
        }
