# Generated by Django 3.1.5 on 2021-02-27 22:30

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields
import main.utilities
import main.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvancedUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='username')),
                ('user_image', models.ImageField(blank=True, upload_to=main.utilities.get_timestamp_path, verbose_name='Фотография пользователя')),
                ('username', models.CharField(error_messages={'unique': 'Користувач з таким іменем уже був зареєстрований раніше.'}, help_text='Вимоги: від шести до двадцяти чотирьох символів (6-24). Букви латинського алфавіту, цифри та символ _', max_length=24, unique=True, validators=[main.validators.username_validator], verbose_name='Нікнейм')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email адреса')),
                ('phone_number', models.CharField(blank=True, max_length=16, null=True, unique=True, validators=[django.core.validators.RegexValidator(regex='^(\\s*)?(\\+)?([- _():=+]?\\d[- _():=+]?){10,14}(\\s*)?$')], verbose_name='Номер телефона')),
                ('date_of_birth', models.CharField(blank=True, max_length=32, null=True, validators=[main.validators.date_of_birth_validator], verbose_name='Дата народження')),
                ('is_activated', models.BooleanField(default=False, help_text='Параметр стає активним, коли користувач підтвердить свою електронну адресу.', verbose_name='Профіль активований через ел.пошту')),
                ('about_me', models.TextField(help_text='Інформація про вас. Інші користувачі зможуть дізнатись про вас більше.', max_length=512, null=True, verbose_name='Про себе')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='VillagesOfBershad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'Населений пункт',
                'verbose_name_plural': 'Населені пункти',
            },
        ),
        migrations.CreateModel(
            name='ChangesInUserInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_first_name', models.CharField(max_length=150, verbose_name="Нове ім'я")),
                ('new_last_name', models.CharField(max_length=150, verbose_name='Нова фамілія')),
                ('new_email', models.EmailField(max_length=254, verbose_name='Нова ел.пошта')),
                ('new_phone_number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(regex='^(\\s*)?(\\+)?([- _():=+]?\\d[- _():=+]?){10,14}(\\s*)?$')], verbose_name='Номер телефона')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='advanceduser',
            name='village',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='main.villagesofbershad', verbose_name='Місто/село'),
        ),
    ]
