# coding: utf-8
import json
import six
from copy import deepcopy

from django import forms
from django.db import transaction

from yaat.models import Column


class HeadersField(forms.Field):
    def to_python(self, value):
        if isinstance(value, six.string_types):
            try:
                return json.loads(value)
            except ValueError:
                raise forms.ValidationError("Enter valid JSON")
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
        retval = deepcopy(self.columns[self._column_fields[name]])
        retval.pk = None
        return retval

    def clean_headers(self):
        posted = self.cleaned_data['headers']

        if not posted:  # posted headers is None
            return self.columns

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

    def save(self):
        if self.columns == self.cleaned_data['headers']:
            return

        for i in range(0, len(self.cleaned_data['headers'])):
            self.cleaned_data['headers'][i].order = i + 1
            self.cleaned_data['headers'][i].user = user

        with transaction.atomic():
            col = self.cleaned_data['headers'][0]
            Column.objects.filter(user_id=col.user_id, resource=col.resource).delete()
            Column.objects.bulk_create(self.cleaned_data['headers'])
