# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordChangeRequired',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='The date the entry was created.', verbose_name='created', db_index=True)),
                ('user', models.OneToOneField(related_name='password_change_required', verbose_name='user', to=settings.AUTH_USER_MODEL, help_text='The user who needs to change his/her password.')),
            ],
            options={
                'ordering': ['-created'],
                'get_latest_by': 'created',
                'verbose_name': 'enforced password change',
                'verbose_name_plural': 'enforced password changes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PasswordHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, help_text='The date the entry was created.', verbose_name='created', db_index=True)),
                ('password', models.CharField(help_text='The encrypted password.', max_length=128, verbose_name='password')),
                ('user', models.ForeignKey(related_name='password_history_entries', verbose_name='user', to=settings.AUTH_USER_MODEL, help_text='The user this password history entry belongs to.')),
            ],
            options={
                'ordering': ['-created'],
                'get_latest_by': 'created',
                'verbose_name': 'password history entry',
                'verbose_name_plural': 'password history entries',
            },
            bases=(models.Model,),
        ),
    ]
