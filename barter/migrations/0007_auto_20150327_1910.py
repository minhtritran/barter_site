# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0006_auto_20150327_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favor',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', default=datetime.datetime(2015, 3, 27, 19, 10, 13, 610043), null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', default=datetime.datetime(2015, 3, 27, 19, 10, 13, 610043), null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', default=datetime.datetime(2015, 3, 27, 19, 10, 13, 610043), null=True),
            preserve_default=True,
        ),
    ]
