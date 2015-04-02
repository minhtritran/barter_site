# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0011_auto_20150327_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favor',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', null=True, default=datetime.datetime(2015, 3, 28, 0, 32, 33, 348862, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', null=True, default=datetime.datetime(2015, 3, 28, 0, 32, 33, 348862, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', null=True, default=datetime.datetime(2015, 3, 28, 0, 32, 33, 348862, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
