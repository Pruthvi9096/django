# Generated by Django 2.2 on 2020-07-27 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitterapp', '0009_material_subject'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Material',
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
    ]
