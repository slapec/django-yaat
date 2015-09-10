# coding: utf-8
import json
import six

from copy import deepcopy
from django import forms

from yaat.models import Column


class HeadersField(forms.Field):
    def to_python(self, value):
        if isinstance(value, six.string_types):
            try:
                return json.loads(value)
            except ValueError:
                raise forms.ValidationError(_("Enter valid JSON"))
        return value


class YaatValidatorForm(forms.Form):
    limit = forms.IntegerField(min_value=0)
    offset = forms.IntegerField(min_value=0, required=False)
    headers = HeadersField(required=False)

    def __init__(self, *args, columns, **kwargs):
        self.columns = columns
        self._column_fields = {self.columns[i].key: i for i in range(0, len(self.columns))}

        super().__init__(*args, **kwargs)

    def _get_column(self, name):
        return self.columns[self._column_fields[name]]

    def clean_headers(self):
        posted = self.cleaned_data['headers']

        headers = deepcopy(self.columns)
        if not posted: # posted headers is None
            return headers

        headers = []
        for head in posted:
            try:
                col = self._get_column(head['key'])
                col.ordering = head['order']
                col.is_shown = not head['hidden']
                headers.append(col)
            except KeyError:
                pass

        return headers