# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 21:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0007_work_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work',
            name='order',
            field=models.IntegerField(default=1, verbose_name='Position on the category page'),
        ),
    ]
