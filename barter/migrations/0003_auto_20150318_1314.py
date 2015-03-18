# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0002_auto_20150318_1240'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='last_edit',
            field=models.DateTimeField(verbose_name='Last Edit', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='offer',
            name='message',
            field=models.CharField(max_length=200, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', null=True),
            preserve_default=True,
        ),
    ]
