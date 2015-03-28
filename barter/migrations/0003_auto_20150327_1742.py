# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0002_auto_20150319_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favor',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', null=True, default=datetime.datetime(2015, 3, 27, 17, 42, 45, 386495)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', null=True, default=datetime.datetime(2015, 3, 27, 17, 42, 45, 386495)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', null=True, default=datetime.datetime(2015, 3, 27, 17, 42, 45, 386495)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(max_length=40, unique=True),
            preserve_default=True,
        ),
    ]
