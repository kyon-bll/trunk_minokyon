# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-03-08 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='geek_point',
            field=models.IntegerField(default=0, verbose_name='ギークポイント'),
        ),
    ]