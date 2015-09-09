# coding: utf-8

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
            Column('get_owner', 'Owner'),
            'name', 'quantity', 'price',
            Column('get_total_price', 'Total price')
        )
