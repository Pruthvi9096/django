# Generated by Django 2.2 on 2020-08-14 03:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitterapp', '0005_event_usage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.RemoveField(
            model_name='member',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='group',
        ),
        migrations.RemoveField(
            model_name='membership',
            name='member',
        ),
        migrations.DeleteModel(
            name='Usage',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
        migrations.DeleteModel(
            name='Member',
        ),
        migrations.DeleteModel(
            name='Membership',
        ),
    ]
