# Generated by Django 5.1.1 on 2024-10-21 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_delete_userchatname'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='custom_name',
            field=models.CharField(default=1, max_length=35),
            preserve_default=False,
        ),
    ]