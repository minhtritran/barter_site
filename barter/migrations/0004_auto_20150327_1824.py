# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0003_auto_20150327_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favor',
            name='message',
            field=models.TextField(max_length=200, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='favor',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name='Date Published', default=datetime.datetime(2015, 3, 27, 18, 24, 6, 760600)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='message',
            field=models.TextField(max_length=200, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name='Date Published', default=datetime.datetime(2015, 3, 27, 18, 24, 6, 760600)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='message',
            field=models.TextField(max_length=200, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='pub_date',
            field=models.DateTimeField(null=True, verbose_name='Date Published', default=datetime.datetime(2015, 3, 27, 18, 24, 6, 760600)),
            preserve_default=True,
        ),
    ]
