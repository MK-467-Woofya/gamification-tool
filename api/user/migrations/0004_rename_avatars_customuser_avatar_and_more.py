# Generated by Django 5.1 on 2024-10-01 03:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_customuser_avatars_customuser_titles'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='avatars',
            new_name='avatar',
        ),
        migrations.RenameField(
            model_name='customuser',
            old_name='titles',
            new_name='title',
        ),
    ]
