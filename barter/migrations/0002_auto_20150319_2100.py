# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('barter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('slug', models.SlugField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='favor',
            name='categories',
        ),
        migrations.AddField(
            model_name='favor',
            name='tags',
            field=models.ManyToManyField(to='barter.Tag'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='favor',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', null=True, default=datetime.datetime(2015, 3, 19, 21, 0, 31, 859896)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', null=True, default=datetime.datetime(2015, 3, 19, 21, 0, 31, 859896)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='offer',
            name='pub_date',
            field=models.DateTimeField(verbose_name='Date Published', null=True, default=datetime.datetime(2015, 3, 19, 21, 0, 31, 859896)),
            preserve_default=True,
        ),
    ]
