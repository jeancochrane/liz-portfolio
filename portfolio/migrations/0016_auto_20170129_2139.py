# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-30 02:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0015_exhibitions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='work',
            old_name='project',
            new_name='parent_project',
        ),
        migrations.AddField(
            model_name='project',
            name='featured_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='portfolio.Work'),
        ),
        migrations.AlterField(
            model_name='project',
            name='featured',
            field=models.BooleanField(default=False, verbose_name='feature this project on the home page'),
        ),
    ]
