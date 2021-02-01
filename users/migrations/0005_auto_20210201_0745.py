# Generated by Django 3.1.1 on 2021-02-01 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0016_auto_20200610_1551'),
        ('users', '0004_auto_20200610_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savepost',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved', to='posts.post'),
        ),
    ]