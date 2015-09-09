# coding: utf-8

from restify.resource.model import ModelResourceOptions
from restify.resource.base import ResourceMeta

from .serializer import YaatModelResourceSerializer


class YaatModelResourceOptions(ModelResourceOptions):
    serializer = YaatModelResourceSerializer
    columns = ()


class YaatModelResourceMeta(ResourceMeta):
    options_class = YaatModelResourceOptions
