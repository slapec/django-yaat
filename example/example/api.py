# coding: utf-8

from restify.api import Api

from yaat_examples.api.resources import ModelExampleResource, ModelComputedExampleResource, Stateful

api = Api(api_name='example')
api.register(regex='model_example/$', resource=ModelExampleResource)
api.register(regex='model_computed_example/$', resource=ModelComputedExampleResource)
api.register(regex='stateful/$', resource=Stateful)
