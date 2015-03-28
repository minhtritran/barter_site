# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0004_auto_20150327_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favor',
            name='message',
            field=models.TextField(default='', max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='favor',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', null=True, default=datetime.datetime(2015, 3, 27, 18, 59, 13, 613252)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='message',
            field=models.TextField(default='', max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', null=True, default=datetime.datetime(2015, 3, 27, 18, 59, 13, 613252)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='message',
            field=models.TextField(default='', max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', null=True, default=datetime.datetime(2015, 3, 27, 18, 59, 13, 613252)),
            preserve_default=True,
        ),
    ]
