# Generated by Django 3.1.5 on 2021-02-26 18:02

from django.db import migrations, models
import main.utilities


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20210222_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='advanceduser',
            name='user_image',
            field=models.ImageField(blank=True, upload_to=main.utilities.get_timestamp_path, verbose_name='Фотография пользователя'),
        ),
    ]
