# Generated by Django 3.0.6 on 2020-05-23 11:10

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20200523_0929'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='choice1',
        ),
        migrations.RemoveField(
            model_name='post',
            name='choice2',
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Art', 'Art'), ('Buisness', 'Buisness'), ('Cooking', 'Cooking'), ('Design', 'Design'), ('Education', 'Education'), ('Engineering', 'Engineering'), ('Entertainment', 'Entertainment'), ('Food', 'Food'), ('Goverment', 'Goverment'), ('Healthcare', 'Healthcare'), ('Languages', 'Languages'), ('Law', 'Law'), ('Mathematics', 'Mathematics'), ('Politics', 'Politics'), ('Science', 'Science'), ('Sports', 'Sports'), ('Technology', 'Technology'), ('Traveling', 'Traveling')], max_length=160, verbose_name='Select tags for your post...'),
        ),
    ]