# Generated by Django 5.0.7 on 2024-09-18 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_users_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
