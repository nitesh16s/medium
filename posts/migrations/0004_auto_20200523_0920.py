# Generated by Django 3.0.6 on 2020-05-23 09:20

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20200523_0919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='choice1',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('1', 'Art'), ('2', 'Buisness'), ('3', 'Cooking'), ('4', 'Design'), ('5', 'Education'), ('6', 'Engineering'), ('7', 'Entertainment'), ('8', 'Food'), ('9', 'Goverment')], max_length=17, verbose_name='Category...'),
        ),
    ]
