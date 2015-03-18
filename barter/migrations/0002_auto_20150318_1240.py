# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agreement',
            name='customOffer',
            field=models.ForeignKey(null=True, to='barter.Offer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agreement',
            name='favor',
            field=models.ForeignKey(to='barter.Favor', null=True, related_name='Agreement Favor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agreement',
            name='receiver',
            field=models.ForeignKey(to='barter.User', null=True, related_name='Agreement Receiver'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agreement',
            name='sender',
            field=models.ForeignKey(to='barter.User', null=True, related_name='Agreement Sender'),
            preserve_default=True,
        ),
    ]
