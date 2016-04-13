# coding: utf-8

import uuid

from django.contrib.auth.models import User
from django.test import TestCase

from yaat.models import Column


class ColumnCachedTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')

    def test_cached_column_order(self):
        columns = []

        for i in range(10):
            column = Column()
            columns.append(column)

            column.order = i
            column.resource = 'test1'
            column.key = str(uuid.uuid4())
            column.is_shown = True
            column.user = self.user

        Column.objects.bulk_create(columns)

        qs = Column.objects.filter(resource='test1', user=self.user)
        print(qs.query)
