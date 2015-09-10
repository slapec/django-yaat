# coding: utf-8

from django.conf.urls import include, url

from . import api
from yaat_examples import views
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    url(r'^$', view=RedirectView.as_view(url='/model_example/')),
    url(r'^model_example/', view=TemplateView.as_view(template_name='yaat_examples/model_example.html'), name='model_example'),
    url(r'^model_computed_example/', view=TemplateView.as_view(template_name='yaat_examples/model_computed_example.html'), name='model_computed_example'),
    url(r'^api/', include(api.api.urls, namespace='api'))
]
