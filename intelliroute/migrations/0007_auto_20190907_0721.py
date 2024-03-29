# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-09-07 07:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("intelliroute", "0006_auto_20190906_2347"),
    ]

    operations = [
        migrations.AddField(
            model_name="requestaudit",
            name="request_url",
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name="requestaudit",
            name="http_method",
            field=models.CharField(
                choices=[
                    ("GET", "Get"),
                    ("POST", "Post"),
                    ("PUT", "Put"),
                    ("DELETE", "Delete"),
                    ("PATCH", "Patch"),
                ],
                max_length=5,
            ),
        ),
    ]
