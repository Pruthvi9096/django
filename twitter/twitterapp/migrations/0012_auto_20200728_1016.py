# Generated by Django 2.2 on 2020-07-28 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitterapp', '0011_attribute_main'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Attribute',
        ),
        migrations.DeleteModel(
            name='Main',
        ),
    ]
