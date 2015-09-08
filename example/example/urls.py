# coding: utf-8

from django.conf.urls import include, url

from . import api
from yaat_examples import views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', view=RedirectView.as_view(url='/model_example/')),
    url(r'^model_example/', view=views.model_example, name='model_example'),
    url(r'^api/', include(api.api.urls, namespace='api'))
]
