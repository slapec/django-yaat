# coding: utf-8

import json
from copy import deepcopy

import six
from django.core.exceptions import ValidationError
from django import forms

from .models import Column


class HeadersField(forms.Field):
    def to_python(self, value):
        if isinstance(value, six.string_types):
            try:
                return json.loads(value)
            except ValueError:
                raise forms.ValidationError('Enter valid JSON')
        return value


class YaatValidatorForm(forms.Form):
    limit = forms.IntegerField(min_value=0)
    offset = forms.CharField(required=False)
    headers = HeadersField(required=False)

    def __init__(self, *args, columns, **kwargs):
        self.columns = columns
        self._column_fields = {column.key: i for i, column in enumerate(self.columns)}

        super().__init__(*args, **kwargs)

    def _get_column(self, name):
        return deepcopy(self.columns[self._column_fields[name]])

    def clean_headers(self):
        posted = self.cleaned_data['headers']

        if not posted:  # posted headers is None
            return self.columns

        headers = []
        for head in posted:
            try:
                # TODO: Add validaton here
                col = self._get_column(head['key'])
                headers.append(col)

                if col.ordering != Column.ORDER_DISALLOWED:
                    col.ordering = head['order']

                if col.is_shown != Column.HIDE_DISALLOWED:
                    col.is_shown = not head['hidden']
            except KeyError:
                pass

        return headers

    def save(self):
        print(self.columns == self.cleaned_data['headers'])
