Getting started
===============

Defining the resource
---------------------

First of all, because the class is called Yaat\ *Model*\ Resource you should have some model to show. So lets define
one.

.. code-block:: python

    from django.db import models


    class Item(models.Model):
        name = models.CharField(max_length=64)
        quantity = models.PositiveIntegerField()
        price = models.PositiveIntegerField()

Also import ``YaatModelResource`` and subclass it. The model class (and some other attributes) is listed in a class
called ``Meta`` **inside** the resource class. You're might already be familiar with this method because Django uses it
too.

.. code-block:: python

    from yaat.resource import YaatModelResource

    class ModelExampleResource(YaatModelResource):
        class Meta:
            resource_name = 'model-example'
            model = Item
            columns = ('name', 'quantity', 'price')

``YaatModelResource`` is very similary to ``restify.resource.ModelResource`` except that it defines some additional
meta attributes. In the above example ``resource_name`` and ``model`` are inherited, but ``columns`` is yaat-only.

Column list is always required (like Django forms require to specify either ``fields`` or ``exclude``). Here you can
list any names that are fields of the ``Item`` model (listed in ``Item._meta.fields``) or you can add ``Column`` objects
too.

That's it, the resource is ready. Now you have to register it as a restify-framework API endopoint.

.. note::

    It is a good idea to create a Python module named ``api`` inside the Django application which has restify-framework
    resources. Put resources in ``api/resources.py`` and custom serializers in ``api/serializers.py``.

Registering the API endpoint
----------------------------
You're not required but it is a good practice to put all API endpoints into a separate file somewhere near
``ROOT_URLCONF``.

.. code-block:: python

    from restify.api import Api

    api = Api(api_name='example')
    api.register(regex='model_example/$', resource=ModelExampleResource)

So here you've registered the resource as any other restify endpoint. Then include the URLs of the API in an urlconf.

.. code-block:: python

    from django.conf.urls import include, url

    urlpatterns = [
        url(r'^api/', include(api.api.urls, namespace='api'))
    ]

And there it is, the endpoint is ready to receive ``POST``\ s.

Connecting the directive to the endpoint
----------------------------------------

This is as easy as the other steps above. In a Django template you can get the URL of every resource under the ``api``
namespace. This is why the ``resource_name`` property is required.

.. code-block:: html

    <yat api="{% url 'api:model-example' %}"></yat>

The ``<yat>`` directive handles everything else for you. If you want to customize that too, head to the
`yaat repository <https://github.com/slapec/yaat>`_.

Working examples
================

You can find working examples in the bundled Django example project in django-yaat's repository.