# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-26 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0023_auto_20170212_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='featured_image',
            field=models.FileField(blank=True, upload_to='about/'),
        ),
        migrations.AlterField(
            model_name='exhibitions',
            name='featured_image',
            field=models.FileField(blank=True, upload_to='exhibitions/'),
        ),
    ]
