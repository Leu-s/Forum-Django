from django.db import models
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField
from .utilities import phone_number_validator
from .utilities import date_of_birth_validator


class AdvancedUser(AbstractUser):
    phone_number = models.CharField(max_length=16, null=True, blank=True,
                                    validators=[phone_number_validator], verbose_name='Номер телефона')
    village = models.OneToOneField(to='VillagesOfBershad', null=True, blank=True, on_delete=models.PROTECT,
                                   verbose_name='Місто/село')
    date_of_birth = models.CharField(max_length=32, null=True, blank=True,
                                     validators=[date_of_birth_validator], verbose_name='Дата народження')
    username_slug = AutoSlugField(populate_from='username')


class VillagesOfBershad(models.Model):
    name = models.CharField(max_length=64, verbose_name='Назва')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Населений пункт'
        verbose_name_plural = 'Населені пункти'




