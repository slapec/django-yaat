# coding: utf-8

import json
from collections import OrderedDict

from django.core.exceptions import FieldDoesNotExist
from django.core.paginator import Paginator
from restify.http.response import ApiResponse
from restify.resource import ModelResource


class YaatModelResource(ModelResource):
    UNORDERED = 0
    ASC = 1
    DESC = 2

    FIELDS = ()
    DISPLAY_NAME_FOR = {}
    PREPEND_COLS = ()
    APPEND_COLS = ()

    def __init__(self, **kwargs):
        super(YaatModelResource, self).__init__(**kwargs)

        self.PREPEND_COLS = OrderedDict(self.PREPEND_COLS)
        self.APPEND_COLS = OrderedDict(self.APPEND_COLS)

        self.VIRTUAL_COLS = self.PREPEND_COLS.copy()
        self.VIRTUAL_COLS.update(self.APPEND_COLS)

        for key, value in self.VIRTUAL_COLS.items():
            if hasattr(self, 'handle_' + key):
                value['handler'] = getattr(self, 'handle_' + key)

    def get_model_fields(self):
        for field in self.FIELDS:
            try:
                yield field, self._meta.model._meta.get_field(field).verbose_name
            except FieldDoesNotExist:
                if field in self.VIRTUAL_COLS:
                    yield field, self.VIRTUAL_COLS[field]['value']
                else:
                    yield field, getattr(self._meta.model, field)

    def get_field_ordering(self, order_obj):
        key = order_obj['key']
        order = order_obj['order']
        ordering = '-' if order == self.DESC else ''
        return ordering + key

    def get_field_verbose_name(self, key):
        return str(self._meta.model._meta.get_field(key).verbose_name)

    def get_queryset(self, order_keys=()):
        return super(YaatModelResource, self).get_queryset().order_by(*order_keys).all()

    def yaat_data(self, post):
        reply = {
            'columns': [],
            'rows': [],
            'pages': {
                'current': 1,
                'list': []
            }
        }

        # Create header row ----------------------------------------------------
        cell_order = []
        order_keys = []
        if 'headers' in post:
            # Structure used to reply paging, sorting, hiding ------------------
            columns = reply['columns']
            for header in post['headers']:
                key = header['key']
                # Skip processing prepend and append columns
                if key in self.VIRTUAL_COLS:
                    columns.append({
                        'key': key,
                        'value': self.VIRTUAL_COLS[key]['value']
                    })
                    cell_order.append(key)
                else:
                    column = {
                        'key': key,
                        'value': self.get_field_verbose_name(key)
                    }
                    columns.append(column)

                    if not header.get('hidden'):
                        cell_order.append(key)
                    else:
                        column['hidden'] = header['hidden']

                    if header.get('order') is not None:
                        column['order'] = header['order']
                        if header['order'] in {self.ASC, self.DESC}:
                            order_keys.append(self.get_field_ordering(header))
        else:
            # Structure used to initialize the table ---------------------------
            columns = reply['columns']

            # Prepend columns
            for key, value in self.PREPEND_COLS.items():
                cell_order.append(key)
                columns.append({
                    'key': key,
                    'value': value['value']
                })

            # Adding real columns
            for key, value in self.get_model_fields():
                cell_order.append(key)
                columns.append({
                    'key': key,
                    'value': str(value),
                    'order': self.UNORDERED
                })

            # Append columns
            for key, value in self.APPEND_COLS.items():
                cell_order.append(key)
                columns.append({
                    'key': key,
                    'value': value['value']
                })

        # Collecting rows ------------------------------------------------------
        limit = int(post['limit'])
        offset = 1 if post['offset'] is None else int(post['offset'])

        qs = self.get_queryset(order_keys)
        paginator = Paginator(qs, limit)
        page = paginator.page(offset)
        rows = reply['rows']
        for obj in page:
            row_values = []
            rows.append({
                'id': obj.pk,
                'values': row_values
            })
            for column_name in cell_order:
                if column_name in self.VIRTUAL_COLS:
                    handler = self.VIRTUAL_COLS[column_name]['handler']
                    value = handler(obj)
                else:
                    if column_name in self.DISPLAY_NAME_FOR:
                        value = getattr(obj, 'get_' + column_name + '_display')()
                    else:
                        value = getattr(obj, column_name)
                    value = str(value)
                row_values.append(value)

        # Paging ---------------------------------------------------------------
        previous = None
        if page.has_previous():
            number = page.previous_page_number()
            previous = {
                'key': number,
                'value': number
            }
        reply['pages']['list'].append(previous)

        # Current page must be at index #1
        reply['pages']['list'].append({
            'key': offset,
            'value': offset
        })

        next = None
        if page.has_next():
            number = page.next_page_number()
            next = {
                'key': number,
                'value': number
            }
        reply['pages']['list'].append(next)

        return reply

    def post(self, request, *args, **kwargs):
        post = json.loads(request.body.decode()) if request.body else None
        data = self.yaat_data(post)
        return ApiResponse(data)
