# Generated by Django 3.1.2 on 2021-02-19 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20210201_0745'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='author',
            new_name='user',
        ),
    ]
