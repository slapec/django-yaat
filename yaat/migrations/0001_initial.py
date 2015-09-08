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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('resource', models.CharField(verbose_name='Resource name', max_length=64)),
                ('order', models.PositiveIntegerField(verbose_name='Column order')),
                ('key', models.CharField(verbose_name='Column key', max_length=64)),
                ('is_shown', models.NullBooleanField(default=True, verbose_name='Show field')),
                ('ordering', models.PositiveSmallIntegerField(choices=[(None, 'Ordering disallowed'), (0, 'Unordered'), (1, 'Ascending'), (2, 'Descending')], default=0, null=True, verbose_name='Field order')),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
