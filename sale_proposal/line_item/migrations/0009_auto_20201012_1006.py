# Generated by Django 2.2 on 2020-10-12 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('line_item', '0008_auto_20201009_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lineitem',
            name='max_discount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]