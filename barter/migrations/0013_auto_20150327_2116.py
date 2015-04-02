# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0012_auto_20150327_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favor',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='Date Published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='Date Published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='Date Published'),
            preserve_default=True,
        ),
    ]
