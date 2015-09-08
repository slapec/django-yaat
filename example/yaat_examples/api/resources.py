# coding: utf-8

from yaat.resource import YaatModelResource
from yaat.models import Column

from yaat_examples.models import Item


class ModelExampleResource(YaatModelResource):
    class Meta:
        resource_name = 'model-example'
        model = Item
        columns = ('id', 'name', 'quantity', 'price')
