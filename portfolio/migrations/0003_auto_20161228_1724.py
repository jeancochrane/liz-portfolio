# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 22:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_auto_20161223_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='featured_image',
            field=models.FileField(upload_to='about/'),
        ),
        migrations.AlterField(
            model_name='work',
            name='statement',
            field=models.TextField(blank=True),
        ),
    ]
