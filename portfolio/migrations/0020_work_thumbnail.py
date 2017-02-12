# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-11 23:11
from __future__ import unicode_literals

from django.db import migrations, models
import portfolio.models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0019_project_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='thumbnail',
            field=models.FileField(blank=True, upload_to=portfolio.models.filepath, verbose_name='upload a thumbnail (optional)'),
        ),
    ]
