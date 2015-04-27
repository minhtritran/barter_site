# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0025_auto_20150427_1700'),
        ('postman', '0002_remove_message_agreement'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='agreement',
            field=models.ForeignKey(blank=True, to='barter.Agreement', null=True),
            preserve_default=True,
        ),
    ]
