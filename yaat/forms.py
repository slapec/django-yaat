# coding: utf-8

from django import forms


class YaatValidatorForm(forms.Form):
    limit = forms.IntegerField(min_value=0)
    offset = forms.CharField(required=False)

    def __init__(self, *args, columns, **kwargs):
        self.columns = columns

        super().__init__(*args, **kwargs)

        # TODO: yaat is inconsistent of expecting 'columns' but replying with 'headers'
        #columns = self.apply_column_states(post.get('headers', None), self.get_columns())

    def apply_column_states(self, states, columns):
        if states:
            # TODO: Add validating here
            column_map = {_.key: _ for _ in columns}

            columns = []
            for state in states:
                column = column_map[state['key']]
                columns.append(column)

                if column.ordering != Column.ORDER_DISALLOWED:
                    column.ordering = state['order']

                if column.is_shown != Column.HIDE_DISALLOWED:
                    column.is_shown = not state['hidden']
        return columns