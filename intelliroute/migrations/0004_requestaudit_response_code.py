# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-09-06 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intelliroute', '0003_auto_20190906_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestaudit',
            name='response_code',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]