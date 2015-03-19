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
            name='Agreement',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('status', models.CharField(default='pending', max_length=16)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Favor',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('last_edit', models.DateTimeField(null=True, verbose_name='Last Edit')),
                ('pub_date', models.DateTimeField(null=True, verbose_name='Date Published')),
                ('message', models.CharField(default='', max_length=200)),
                ('title', models.CharField(default='', max_length=32)),
                ('categories', models.CommaSeparatedIntegerField(max_length=16)),
                ('allow_offers', models.BooleanField(default=False)),
                ('status', models.CharField(default='open', max_length=16)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('last_edit', models.DateTimeField(null=True, verbose_name='Last Edit')),
                ('pub_date', models.DateTimeField(null=True, verbose_name='Date Published')),
                ('message', models.CharField(default='', max_length=200)),
                ('rating', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('pub_date', models.DateTimeField(verbose_name='Date Published')),
                ('favor', models.ForeignKey(related_name='Offers Favor', to='barter.Favor')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, parent_link=True, to=settings.AUTH_USER_MODEL, serialize=False, primary_key=True)),
                ('DOB', models.DateField(verbose_name='Date of Birth')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
        ),
        migrations.AddField(
            model_name='offer',
            name='sender',
            field=models.ForeignKey(to='barter.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedback',
            name='receiver',
            field=models.ForeignKey(related_name='Feedback Receiver', to='barter.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedback',
            name='sender',
            field=models.ForeignKey(related_name='Feedback Sender', to='barter.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='favor',
            name='author',
            field=models.ForeignKey(related_name='Author', to='barter.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='favor',
            name='completed_by',
            field=models.ForeignKey(related_name='Completed by', default=None, to='barter.User'),
            preserve_default=True,
        ),
    ]
