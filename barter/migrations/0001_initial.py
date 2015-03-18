# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('last_edit', models.DateTimeField(verbose_name='Last Edit')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('message', models.CharField(max_length=200)),
                ('title', models.CharField(default='', max_length=32)),
                ('categories', models.CommaSeparatedIntegerField(max_length=16)),
                ('allow_offers', models.BooleanField(default=False)),
                ('status', models.CharField(default='', max_length=16)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('last_edit', models.DateTimeField(verbose_name='Last Edit')),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('message', models.CharField(max_length=200)),
                ('rating', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, to=settings.AUTH_USER_MODEL, parent_link=True, serialize=False, primary_key=True)),
                ('DOB', models.DateField(verbose_name='Date of Birth')),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
        migrations.AddField(
            model_name='feedback',
            name='receiver',
            field=models.ForeignKey(to='barter.User', related_name='Receiver'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedback',
            name='sender',
            field=models.ForeignKey(to='barter.User', related_name='Sender'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='favor',
            name='author',
            field=models.ForeignKey(to='barter.User', related_name='Author'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='favor',
            name='completed_by',
            field=models.ForeignKey(to='barter.User', related_name='Completed by', default=None),
            preserve_default=True,
        ),
    ]
