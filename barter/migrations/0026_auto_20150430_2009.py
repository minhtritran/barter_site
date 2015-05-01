# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0025_auto_20150427_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favor',
            name='message',
            field=models.TextField(max_length=1500, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='favor',
            name='title',
            field=models.CharField(max_length=100, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='message',
            field=models.TextField(max_length=1500, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='message',
            field=models.TextField(max_length=1500, default=''),
            preserve_default=True,
        ),
    ]
