# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0014_auto_20150327_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favor',
            name='author',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='favors_authored'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='favor',
            name='completed_by',
            field=models.ForeignKey(null=True, related_name='favors_completed', to=settings.AUTH_USER_MODEL, default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='receiver',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='feedbacks_received'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='sender',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='feedbacks_sent'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='favor',
            field=models.ForeignKey(to='barter.Favor', related_name='offers'),
            preserve_default=True,
        ),
    ]
