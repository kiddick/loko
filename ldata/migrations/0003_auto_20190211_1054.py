# Generated by Django 2.1.5 on 2019-02-11 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ldata', '0002_branch_trains'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mileage',
            name='km',
            field=models.FloatField(),
        ),
    ]