# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-09-06 21:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("intelliroute", "0004_requestaudit_response_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="integratingapp",
            name="base_url",
            field=models.CharField(default="http://", max_length=100),
            preserve_default=False,
        ),
    ]
