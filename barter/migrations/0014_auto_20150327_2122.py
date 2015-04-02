# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0013_auto_20150327_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favor',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Published'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Date Published'),
            preserve_default=True,
        ),
    ]
