from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .utilities import available_birth_years
from .models import AdvancedUser


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

    # def clean_password1(self):
    #     password1 = self.cleaned_data['password1']
    #     if password1:
    #         password_validation.validate_password(password=password1)
    #     !!!Не возбуждается ValidationError() если пароль не прошел валидацию
    #     return password1

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1:
            password_validation.validate_password(password=password1)
        if password1 and password2 \
                and password1 != password2:
            errors = {
                'password2': ValidationError(
                    'Паролі не співпали',
                    code='password_mismatch'
                )
            }
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = AdvancedUser
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )


class UserPersonalInformationForm(forms.ModelForm):
    class Meta:
        model = AdvancedUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'village',
            'date_of_birth',
        )

        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=available_birth_years()),
        }
