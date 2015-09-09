# coding: utf-8

from restify.serializers import BaseSerializer

from .types import YaatData


class YaatModelResourceSerializer(BaseSerializer):
    # TODO: Split serialization
    def flatten(self, data):
        if isinstance(data, YaatData):
            reply = {
                'columns': [],
                'rows': [],
                'pages': {
                    'current': 1,
                    'list': []
                }
            }

            # Columns ----------------------------------------------------------
            visible_columns = 0
            for column in data.columns:
                reply['columns'].append(column.as_dict())
                if column.is_shown:
                    visible_columns += 1

            # Rows -------------------------------------------------------------
            for row in data.rows:
                if len(row.cells) != visible_columns:
                    raise ValueError('Row cell count differs from visible column count.')
                reply['rows'].append({
                    'id': row.id,
                    'values': row.cells
                })

            # Paging -----------------------------------------------------------
            # TODO: Paging is not so dynamic
            page = data.page

            previous = None
            if data.page.has_previous():
                number = page.previous_page_number()
                previous = {
                    'key': number,
                    'value': number
                }
            reply['pages']['list'].append(previous)

            # Current page must be at index #1 (because reply['pages']['current'] is initialized to 1)
            reply['pages']['list'].append({
                'key': page.number,
                'value': page.number
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
