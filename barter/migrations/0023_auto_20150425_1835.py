# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0022_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agreement',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='agreement',
            name='sender',
        ),
        migrations.AddField(
            model_name='agreement',
            name='accepter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agreement',
            name='favor',
            field=models.ForeignKey(to='barter.Favor', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agreement',
            name='status',
            field=models.CharField(default=b'open', max_length=16),
            preserve_default=True,
        ),
    ]
