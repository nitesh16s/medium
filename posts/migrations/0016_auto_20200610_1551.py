# Generated by Django 3.0.7 on 2020-06-10 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_auto_20200610_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(verbose_name='Comment goes here...'),
        ),
        migrations.AlterField(
            model_name='reply',
            name='content',
            field=models.TextField(verbose_name='Reply goes here...'),
        ),
    ]
