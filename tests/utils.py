# coding: utf-8

from unittest import mock

from django.test import RequestFactory

from yaat.models import Column
from yaat.resource import YaatModelResource


def generate_columns(user=None):
    retval = [
        Column(resource='test_resource', key='first', value='First', is_shown=True, ordering=Column.ASC),
        Column(resource='test_resource', key='second', value='Second', is_shown=True, ordering=Column.ASC),
        Column(resource='test_resource', key='third', value='Third', is_shown=True, ordering=Column.ASC)
    ]

    if user:
        for i in range(0, len(retval)):
            retval[i].user = user

    return retval


def generate_request(user=None):
    factory = RequestFactory()

    request = factory.request()
    request.session = dict()

    if user:
        request.user = user
    else:
        request.user = mock.MagicMock()

    return request


def generate_resource():
    resource = mock.MagicMock()

    resource._meta = mock.MagicMock()
    resource._meta.limit = None

    return resource


class StatefulResource(YaatModelResource):
    class Meta:
        resource_name = 'test-resource'
        stateful_init = True

