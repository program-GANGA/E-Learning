# Generated by Django 4.2.16 on 2024-10-03 21:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0002_trainer_password_trainer_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainer',
            name='password',
        ),
        migrations.RemoveField(
            model_name='trainer',
            name='username',
        ),
    ]
