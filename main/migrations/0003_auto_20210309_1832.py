# Generated by Django 3.1.5 on 2021-03-09 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210228_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changesinuserinformation',
            name='new_first_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name="Нове ім'я"),
        ),
        migrations.AlterField(
            model_name='changesinuserinformation',
            name='new_last_name',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Нова фамілія'),
        ),
    ]