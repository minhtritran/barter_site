# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0005_auto_20150318_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favor',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', default=datetime.datetime(2015, 3, 18, 17, 13, 8, 410817), null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', default=datetime.datetime(2015, 3, 18, 17, 13, 8, 410817), null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', default=datetime.datetime(2015, 3, 18, 17, 13, 8, 410817), null=True),
            preserve_default=True,
        ),
    ]
