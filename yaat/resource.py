# coding: utf-8

from django.core.paginator import Paginator
from restify.http import status
from restify.http.response import ApiResponse
from restify.resource import Resource
from restify.resource.model import ModelResourceMixin

from .forms import YaatValidatorForm
from .meta import YaatModelResourceMeta
from .models import Column
from .types import YaatData, YaatRow


class YaatModelResource(Resource, ModelResourceMixin, metaclass=YaatModelResourceMeta):
    def get_columns(self):
        columns = []
        for c in self._meta.columns:
            if isinstance(c, str):
                field = self._meta.model._meta.get_field(c)
                column = Column(field.name, field.verbose_name, resource=self._meta.resource_name, is_virtual=False)
                columns.append(column)
            elif isinstance(c, Column):
                c.resource = self._meta.resource_name
                columns.append(c)
            else:
                raise TypeError('Column item is expected to be string or Column')
        return columns

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

    def get_page(self, qs, limit, page_number):
        if not page_number:
            page_number = 1
        paginator = Paginator(qs, limit)
        return paginator.page(page_number)

    def get_rows(self, page, cols):
        rows = []
        for obj in page:
            cells = []
            for col in cols:
                if col.is_shown:
                    value = getattr(obj, col.key)
                    cells.append(value)
            rows.append(YaatRow(obj.pk, cells))
        return rows

    def post(self, request, *args, **kwargs):
        columns = self.get_columns()
        form = YaatValidatorForm(request.POST, columns=columns)
        if form.is_valid():
            queryset = self.get_queryset(columns)
            page = self.get_page(queryset, form.cleaned_data['limit'], form.cleaned_data['offset'])
            rows = self.get_rows(page, columns)
            data = YaatData(columns, rows, page)
            return ApiResponse(data)
        else:
            return ApiResponse(form, status_code=status.HTTP_400_BAD_REQUEST)
