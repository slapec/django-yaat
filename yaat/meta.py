# coding: utf-8

from restify.resource.model import ModelResourceOptions
from restify.resource.base import ResourceMeta
from restify.serializers import DjangoSerializer


class YaatModelResourceOptions(ModelResourceOptions):
    serializer = DjangoSerializer
    columns = ()
    stateful = False
    stateful_init = False
    limit = 25
    limit_choices = [25]


class YaatModelResourceMeta(ResourceMeta):
    options_class = YaatModelResourceOptions
