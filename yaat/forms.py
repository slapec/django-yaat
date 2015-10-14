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
                raise forms.ValidationError('Enter valid JSON')
        return value


class YaatValidatorForm(forms.Form):
    limit = forms.IntegerField(min_value=0, initial=10)
    offset = forms.IntegerField(min_value=0, initial=1)
    headers = HeadersField(required=False)

    def __init__(self, *args, request, columns, stateful_init, **kwargs):
        self.request = request
        self.user = request.user
        self.columns = columns
        self.stateful_init = stateful_init
        self._column_fields = {column.key: i for i, column in enumerate(self.columns)}

        super().__init__(*args, **kwargs)

    def _get_column(self, name):
        retval = deepcopy(self.columns[self._column_fields[name]])
        retval.pk = None
        return retval

    def full_clean(self):
        super().full_clean()
        is_init = False

        if 'limit' in self._errors.keys():
            self.cleaned_data['limit'] = self.fields['limit'].initial
            del self._errors['limit']

        if 'offset' in self._errors.keys():
            self.cleaned_data['offset'] = self.fields['offset'].initial
            del self._errors['offset']

        if 'headers' in self._errors.keys():
            is_init = True
            self.cleaned_data['headers'] = self.columns
            del self._errors['headers']

        if self.stateful_init:
            state = {
                'limit': self.cleaned_data['limit'],
                'offset': self.cleaned_data['offset']
            }

            if is_init:
                # TODO: This is incomplete
                session = self.request.session.get(self.session_key, state)
                if session['limit'] == self.cleaned_data['limit']:
                    self.cleaned_data['limit'] = session['limit']
                    self.cleaned_data['offset'] = session['offset']
                else:
                    self.request.session[self.session_key] = state
            else:
                self.request.session[self.session_key] = state

    @property
    def session_key(self):
        return 'yaat_init_state'

    def clean_headers(self):
        posted = self.cleaned_data['headers']

        headers = []

        try:
            for head in posted:
                try:
                    col = self._get_column(head['key'])
                    headers.append(col)

                    if col.ordering != Column.ORDER_DISALLOWED:
                        col.ordering = head['order']

                    if col.is_shown != Column.HIDE_DISALLOWED:
                        col.is_shown = not head['hidden']
                except KeyError as k:
                    raise forms.ValidationError('Missing property {0!r}'.format(k))
        except TypeError:
            raise forms.ValidationError('Missing headers')

        return headers

    def save(self):
        if self.columns == self.cleaned_data['headers']:
            return

        for i in range(0, len(self.cleaned_data['headers'])):
            self.cleaned_data['headers'][i].order = i + 1
            self.cleaned_data['headers'][i].user = self.user

        with transaction.atomic():
            col = self.cleaned_data['headers'][0]
            Column.objects.filter(user_id=col.user_id, resource=col.resource).delete()
            Column.objects.bulk_create(self.cleaned_data['headers'])
            Column.cached.bulk_create(self.cleaned_data['headers'])
