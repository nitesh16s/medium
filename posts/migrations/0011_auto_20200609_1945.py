# Generated by Django 3.0.7 on 2020-06-09 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20200609_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(verbose_name='Content...'),
        ),
    ]