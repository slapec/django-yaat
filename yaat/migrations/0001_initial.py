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
            name='Column',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('resource', models.CharField(max_length=64, verbose_name='Resource name')),
                ('key', models.CharField(max_length=64, verbose_name='Column key')),
                ('is_shown', models.NullBooleanField(verbose_name='Show field', default=True)),
                ('ordering', models.PositiveSmallIntegerField(null=True, choices=[(None, 'Ordering disallowed'), (0, 'Unordered'), (1, 'Ascending'), (2, 'Descending')], verbose_name='Field order', default=0)),
                ('user', models.ForeignKey(related_name='column_users', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='column',
            unique_together=set([('resource', 'user', 'key')]),
        ),
    ]
