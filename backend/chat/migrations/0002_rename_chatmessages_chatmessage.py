# Generated by Django 5.0.7 on 2024-08-01 12:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChatMessages',
            new_name='ChatMessage',
        ),
    ]