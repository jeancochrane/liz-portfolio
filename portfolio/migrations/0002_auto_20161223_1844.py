# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-23 23:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='about',
            name='site',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sites.Site'),
        ),
    ]
