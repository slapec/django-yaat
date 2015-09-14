# coding: utf-8

from django.contrib.auth.models import User

from yaat.resource import YaatModelResource
from yaat.models import Column
from yaat_examples.models import Item, SmartItem


class ModelExampleResource(YaatModelResource):
    class Meta:
        resource_name = 'model-example'
        model = Item
        columns = ('name', 'quantity', 'price')


class ModelComputedExampleResource(YaatModelResource):
    class Meta:
        resource_name = 'model-computed-example'
        model = SmartItem
        columns = (
            Column(key='get_owner', value='Owner'),
            'name', 'quantity', 'price',
            Column(key='get_total_price', value='Total price')
        )


class Stateful(YaatModelResource):
    class Meta:
        resource_name = 'stateful'
        model = Item
        columns = ('name', 'quantity', 'price')
        stateful = True

    def common(self, request, *args, **kwargs):
        usr, _ = User.objects.get_or_create(username='user')
        request.user = usr
        super().common(request, *args, **kwargs)
