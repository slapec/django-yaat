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
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('resource', models.CharField(max_length=64, verbose_name='Resource name')),
                ('order', models.PositiveIntegerField(verbose_name='Column order')),
                ('key', models.CharField(max_length=64, verbose_name='Column key')),
                ('is_shown', models.NullBooleanField(default=True, verbose_name='Show field')),
                ('ordering', models.PositiveSmallIntegerField(null=True, verbose_name='Field order', default=0, choices=[(None, 'Ordering disallowed'), (0, 'Unordered'), (1, 'Ascending'), (2, 'Descending')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
