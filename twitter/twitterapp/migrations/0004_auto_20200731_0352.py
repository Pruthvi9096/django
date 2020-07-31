# Generated by Django 2.2 on 2020-07-31 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitterapp', '0003_auto_20200730_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('join_date', models.DateTimeField(null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twitterapp.Group')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twitterapp.Member')),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='groups',
            field=models.ManyToManyField(through='twitterapp.Membership', to='twitterapp.Group'),
        ),
    ]