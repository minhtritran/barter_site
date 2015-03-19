# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(default=None, max_length=30, blank=True, null=True)),
                ('last_name', models.CharField(default=None, max_length=30, blank=True, null=True)),
                ('date_of_birth', models.DateField(default=None, null=True, blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('gender', models.CharField(max_length=1, default='m', choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Other')])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('status', models.CharField(max_length=16, default='pending')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Favor',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('last_edit', models.DateTimeField(null=True, verbose_name='Last Edit')),
                ('pub_date', models.DateTimeField(null=True, default=datetime.datetime(2015, 3, 18, 20, 17, 43, 623923), verbose_name='Date Published')),
                ('message', models.CharField(max_length=200, default='')),
                ('title', models.CharField(max_length=32, default='')),
                ('categories', models.CommaSeparatedIntegerField(max_length=16)),
                ('allow_offers', models.BooleanField(default=False)),
                ('status', models.CharField(max_length=16, default='open')),
                ('author', models.ForeignKey(related_name='Author', to=settings.AUTH_USER_MODEL)),
                ('completed_by', models.ForeignKey(related_name='Completed by', default=None, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('last_edit', models.DateTimeField(null=True, verbose_name='Last Edit')),
                ('pub_date', models.DateTimeField(null=True, default=datetime.datetime(2015, 3, 18, 20, 17, 43, 623923), verbose_name='Date Published')),
                ('message', models.CharField(max_length=200, default='')),
                ('rating', models.IntegerField(default=0)),
                ('receiver', models.ForeignKey(related_name='Feedback Receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='Feedback Sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('last_edit', models.DateTimeField(null=True, verbose_name='Last Edit')),
                ('pub_date', models.DateTimeField(null=True, default=datetime.datetime(2015, 3, 18, 20, 17, 43, 623923), verbose_name='Date Published')),
                ('message', models.CharField(max_length=200, default='')),
                ('favor', models.ForeignKey(related_name='Offers Favor', to='barter.Favor')),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='agreement',
            name='customOffer',
            field=models.ForeignKey(to='barter.Offer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agreement',
            name='favor',
            field=models.ForeignKey(related_name='Agreement Favor', to='barter.Favor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agreement',
            name='receiver',
            field=models.ForeignKey(related_name='Agreement Receiver', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agreement',
            name='sender',
            field=models.ForeignKey(related_name='Agreement Sender', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
