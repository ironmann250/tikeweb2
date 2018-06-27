# Generated by Django 2.0.4 on 2018-06-15 06:54

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tikeshell', '0008_auto_20180607_1210'),
    ]

    operations = [
        migrations.CreateModel(
            name='badgetype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('badge_type', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
                ('Content', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='other_events',
            name='image',
            field=models.ImageField(default=0, upload_to='event'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='other_events',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 15, 8, 54, 12, 523219)),
        ),
        migrations.AlterField(
            model_name='show',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 15, 8, 54, 12, 523219)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 15, 8, 54, 12, 538713)),
        ),
        migrations.AddField(
            model_name='badgetype',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tikeshell.Other_events'),
        ),
    ]
