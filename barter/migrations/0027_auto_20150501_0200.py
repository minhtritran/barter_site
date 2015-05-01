# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0026_auto_20150430_2009'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favor',
            options={'ordering': ['-pub_date']},
        ),
    ]
