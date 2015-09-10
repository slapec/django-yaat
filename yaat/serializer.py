# coding: utf-8

from django import forms
from django.core.paginator import Page
from restify.serializers import DjangoSerializer

from .types import YaatData


class YaatModelResourceSerializer(DjangoSerializer):
    pass

    """
    # TODO: Split serialization
    def flatten(self, data):
        if isinstance(data, Page):
            retval = {
                'current': 1,
                'list': []
            }

            previous = None
            if data.has_previous():
                number = data.previous_page_number()
                previous = {
                    'key': number,
                    'value': number
                }
            retval['list'].append(previous)

            # Current page must be at index #1 (because reply['pages']['current'] is initialized to 1)
            retval['list'].append({
                'key': data.number,
                'value': data.number
            })

            next = None
            if data.has_next():
                number = data.next_page_number()
                next = {
                    'key': number,
                    'value': number
                }
            retval['list'].append(next)
            return retval
        else:
            data = super().flatten(data)
            return data"""