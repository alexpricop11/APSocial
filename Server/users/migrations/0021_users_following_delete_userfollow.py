# Generated by Django 5.1.1 on 2024-10-15 18:17

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_userfollow'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserFollow',
        ),
    ]
