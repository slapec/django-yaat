# coding: utf-8

from django.core.paginator import Paginator
from django.contrib.auth.models import AnonymousUser
from restify.http import status
from restify.http.response import ApiResponse
from restify.resource import Resource
from restify.resource.model import ModelResourceMixin

from .forms import YaatValidatorForm
from .meta import YaatModelResourceMeta
from .models import Column


class YaatModelResource(Resource, ModelResourceMixin, metaclass=YaatModelResourceMeta):
    def get_columns(self):
        stateful_columns, columns = [], []
        if self._meta.stateful and not isinstance(self.request.user, AnonymousUser):
            stateful_columns = list(Column.objects.filter(resource=self._meta.resource_name, user=self.request.user)\
                                                  .order_by('order'))

        mapper = {}
        for c in self._meta.columns:
            if isinstance(c, str):
                field = self._meta.model._meta.get_field(c)
                column = Column(key=field.name,
                                value=field.verbose_name,
                                resource=self._meta.resource_name,
                                is_virtual=False)
                columns.append(column)
                mapper[column.key] = len(columns)
            elif isinstance(c, Column):
                c.resource = self._meta.resource_name
                columns.append(c)
                mapper[c.key] = len(columns)
            else:
                raise TypeError('Column item is expected to be string or Column')

        for col in stateful_columns:
            col.value = columns[mapper[col.key] - 1].value

        return stateful_columns or columns

    def get_queryset_order_keys(self, columns):
        keys = []
        for column in columns:
            ordering = column.get_ordering()
            if ordering:
                keys.append(ordering)
        return keys

    def get_queryset(self, columns):
        order_keys = self.get_queryset_order_keys(columns)
        return super().get_queryset().order_by(*order_keys).all()

    def get_page(self, qs, limit, page_number=1):
        paginator = Paginator(qs, limit)
        return paginator.page(page_number)

    def get_rows(self, page, cols, **kwargs):
        rows = []
        for obj in page:
            cells = []
            for col in cols:
                if col.is_shown:
                    value = getattr(obj, col.key)
                    if hasattr(value, '__call__'):
                        value = value(**kwargs)
                    cells.append(value)
            rows.append({'id': obj.pk, 'values': cells})
        return rows

    def post(self, request, *args, **kwargs):
        available_columns = self.get_columns()
        form = YaatValidatorForm(request.POST, columns=available_columns)
        if form.is_valid():
            queryset = self.get_queryset(form.cleaned_data['headers'])
            page = self.get_page(queryset, form.cleaned_data['limit'], form.cleaned_data['offset'])
            rows = self.get_rows(page, form.cleaned_data['headers'])

            if self._meta.stateful and not isinstance(request.user, AnonymousUser):
                form.save(request.user)

            return ApiResponse({'columns': form.cleaned_data['headers'],
                                'rows': rows,
                                'pages': page})
        else:
            return ApiResponse(form, status_code=status.HTTP_400_BAD_REQUEST)
