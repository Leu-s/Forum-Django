from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField
from .validators import phone_number_validator
from .validators import date_of_birth_validator
from .validators import username_validator


class AdvancedUser(AbstractUser):
    slug = AutoSlugField(populate_from='username')
    username = models.CharField(
        max_length=24,
        unique=True,
        help_text=('Вимоги: від шести до двадцяти чотирьох символів (6-24). '
                   'Букви латинського алфавіту, цифри та символ _'),
        validators=[username_validator],
        error_messages={
            'unique': "Користувач з таким іменем уже був зареєстрований раніше.",
        },
        verbose_name='Нікнейм'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email адреса'
    )
    phone_number = models.CharField(
        max_length=16,
        unique=True,
        null=True,
        blank=True,
        validators=[phone_number_validator],
        verbose_name='Номер телефона'
    )
    village = models.OneToOneField(
        to='VillagesOfBershad',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Місто/село'
    )
    date_of_birth = models.CharField(
        max_length=32,
        null=True,
        blank=True,
        validators=[date_of_birth_validator],
        verbose_name='Дата народження',
    )
    is_active = models.BooleanField(
        default=False,
        help_text='Підтвердіть свій аккаунт, перейшовши за посиланням,'
                  ' яку було надіслано на Вашу email адресу.',
        )


class VillagesOfBershad(models.Model):
    name = models.CharField(
        max_length=64,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Населений пункт'
        verbose_name_plural = 'Населені пункти'




