# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-09 19:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IFoxHuntGame', '0004_group_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='powerup',
            name='taken',
            field=models.IntegerField(default=0),
        ),
    ]