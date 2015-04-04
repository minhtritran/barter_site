# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0015_auto_20150404_1644'),
    ]

    operations = [
        migrations.RenameField(
            model_name='offer',
            old_name='sender',
            new_name='trader',
        ),
        migrations.AddField(
            model_name='offer',
            name='made_by_asker',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
