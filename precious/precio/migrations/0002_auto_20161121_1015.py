# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-21 12:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('precio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudaumento',
            name='vigencia_desde',
            field=models.DateField(default=datetime.datetime(2016, 11, 21, 12, 15, 37, 436252, tzinfo=utc)),
        ),
    ]