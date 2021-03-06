from django.db import models
from django.dispatch import Signal
from django.contrib.auth.models import AbstractUser
from django_extensions.db.fields import AutoSlugField
from .validators import phone_number_validator
from .validators import date_of_birth_validator
from .validators import username_validator
from .utilities import get_timestamp_path
from .utilities import send_activation_notification
from .utilities import slugify_function
import re

user_registrated = Signal(providing_args=['instance'])


def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])


user_registrated.connect(user_registrated_dispatcher)


class AdvancedUser(AbstractUser):
    slug = AutoSlugField(populate_from='username')
    user_image = models.ImageField(
        blank=True,
        upload_to=get_timestamp_path,
        verbose_name='Фотография пользователя')
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
    village = models.ForeignKey(
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
    is_activated = models.BooleanField(
        default=False,
        verbose_name='Профіль активований через ел.пошту',
        help_text='Параметр стає активним, коли користувач підтвердить свою електронну адресу.'
    )
    about_me = models.TextField(
        null=True,
        max_length=512,
        verbose_name='Про себе',
        help_text='Інформація про вас. Інші користувачі зможуть дізнатись про вас більше.'
    )


class ChangesInUserInformation(models.Model):
    """
    Temporarily saving new user data, before changing basic information.
    The entry will be deleted after the user confirms the action via email.
    """
    user = models.OneToOneField(AdvancedUser, on_delete=models.CASCADE)
    new_first_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Нове ім'я")
    new_last_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Нова фамілія")
    new_email = models.EmailField(verbose_name='Нова ел.пошта')
    new_phone_number = models.CharField(
        max_length=16,
        null=True,
        validators=[phone_number_validator],
        verbose_name='Номер телефона',
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


class Article(models.Model):
    slug = AutoSlugField(
        populate_from='title',
        db_index=True,
        slugify_function=slugify_function
    )
    author = models.ForeignKey(
        AdvancedUser,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    title = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Заголовок'
    )
    content = models.TextField(
        max_length=2500,
        verbose_name='Стаття'
    )
    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публікації'
    )
    category = models.ForeignKey(
        to='Category',
        default=None,
        on_delete=models.PROTECT,
        db_index=True,
        verbose_name='Категорія'
    )

    class Meta:
        ordering = ['-published']
        verbose_name = 'Стаття'
        verbose_name_plural = 'Статті'

    def __str__(self):
        return self.title


class Category(models.Model):
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='child_category',
        on_delete=models.PROTECT
    )
    title = models.CharField(max_length=50, verbose_name='Назва')
    slug = AutoSlugField(populate_from='title', slugify_function=slugify_function)

    def __str__(self):
        name = f'{self.parent}/{self.title}'
        return re.sub('None/', '', name)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        ordering = ['title']




