# Generated by Django 2.0.4 on 2018-06-07 10:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tikeshell', '0007_auto_20180606_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='other_events',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 7, 12, 10, 36, 778755)),
        ),
        migrations.AlterField(
            model_name='other_events',
            name='register_url',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 7, 12, 10, 36, 782761)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 7, 12, 10, 36, 791771)),
        ),
    ]
