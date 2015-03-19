# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0004_user_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favor',
            name='completed_by',
            field=models.ForeignKey(null=True, to='barter.User', default=None, related_name='Completed by'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='favor',
            name='pub_date',
            field=models.DateTimeField(null=True, default=datetime.datetime(2015, 3, 18, 17, 9, 17, 835012), verbose_name='Date Published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='pub_date',
            field=models.DateTimeField(null=True, default=datetime.datetime(2015, 3, 18, 17, 9, 17, 835012), verbose_name='Date Published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='pub_date',
            field=models.DateTimeField(null=True, default=datetime.datetime(2015, 3, 18, 17, 9, 17, 835012), verbose_name='Date Published'),
            preserve_default=True,
        ),
    ]
