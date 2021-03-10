# Generated by Django 3.1.5 on 2021-03-09 22:44

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_article'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='slug',
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Назва')),
                ('slug', django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='title')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='child_category', to='main.category')),
            ],
        ),
    ]