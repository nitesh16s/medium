# Generated by Django 3.0.6 on 2020-05-23 09:29

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20200523_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='choice1',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Art', 'Art'), ('Buisness', 'Buisness'), ('Cooking', 'Cooking'), ('Design', 'Design'), ('Education', 'Education'), ('Engineering', 'Engineering'), ('Entertainment', 'Entertainment'), ('Food', 'Food'), ('Goverment', 'Goverment')], max_length=78, verbose_name='Category...'),
        ),
        migrations.AlterField(
            model_name='post',
            name='choice2',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Healthcare', 'Healthcare'), ('Languages', 'Languages'), ('Law', 'Law'), ('Mathematics', 'Mathematics'), ('Politics', 'Politics'), ('Science', 'Science'), ('Sports', 'Sports'), ('Technology', 'Technology'), ('Traveling', 'Traveling')], max_length=81, verbose_name='Category...'),
        ),
    ]
