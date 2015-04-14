# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0018_auto_20150404_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agreement',
            name='favor',
            field=models.ForeignKey(related_name='agreement_favor', to='barter.Favor', null=True),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='receiver',
            field=models.ForeignKey(related_name='agreement_receiver', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='agreement',
            name='sender',
            field=models.ForeignKey(related_name='agreement_sender', to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
    ]
