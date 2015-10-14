Advanced resources
==================

Custom columns
--------------

In the meta class of the resource you can list either strings or ``Column`` objects under the ``columns`` property.
String keys must always match a field of the model. ``Column`` keys however are free to have any values. ``Column``
objects have the property ``key`` which is going to be used for model property or method lookup. This is very useful to
send values of related models or computed values in the ``POST``.

Let's say we have the following models:

.. code-block:: python

    class Owner(models.Model):
        name = models.CharField(max_length=64)


    class SmartItem(models.Model):
        owner = models.ForeignKey(Owner)
        name = models.CharField(max_length=64)
        quantity = models.PositiveIntegerField()
        price = models.PositiveIntegerField()

        @property
        def get_total_price(self):
            return self.quantity * self.price

        @property
        def get_owner(self):
            return self.owner.name

Here we've created a simple relation between ``SmartItem`` and ``Owner`` so I can show you how to send related values
too but it is super easy.

So there are 2 property methods ``get_total_price`` and ``get_owner``. To create a resource for this define the
following resource:

.. code-block:: python

    from yaat.models import Column

    class ModelComputedExampleResource(YaatModelResource):
        class Meta:
            resource_name = 'model-computed-example'
            model = SmartItem
            columns = (
                Column(key='get_owner', value='Owner'),
                'name', 'quantity', 'price',
                Column(key='get_total_price', value='Total price')
            )

First you have to import the ``Column`` model. ``Column`` objects are going to be mapped to properties or methods of the
model of the resource by their key (``key`` argument). So in this example when the resource iterates over the queryset
it will get ``get_owner`` **property** of the model first, then ``name``, ``quantity``, ``prce`` **fields** of the
model, then ``get_total_price`` **property** of the model at the end. Those properties and methods that are invoked by
the ``Columns`` are called *handlers*.

We call these columns *virtual* meaning that you can't order by their values out of box (because the ORM can't handle
it). You are allowed to create *non-virtual* columns too but then you must implement the sorting method of those
objects.

However the ``Column`` class is a Django model but it's never stored anywhere unless you mark the resource to be
*stateful*.

Passing values to handlers
--------------------------

Sometimes it is useful to pass an object to a column handler e.g. when you want the model to access the ``User``
instance (``request.user``)

Let's modify the method ``SmartItem.get_total_price`` from the previous example.

.. code-block:: python

        def get_total_price(self, currency):
            return self.quantity * self.price * currency

It's quite trivial but let's say that you want to calculate the ``Item``'s total price based on the logged in user's
currency settings. Note that the method is no longer decorated: you can't pass values to properties.

To pass the value to the handler you have to override the ``get_rows`` method of the resource class
``ModelComputedExampleResource``:

.. code-block:: python

        def get_rows(self, *args):
            return super().get_rows(*args, currency=request.user.currency)

Here you simply invoke the method from the parent class, pass all arguments and your own value as a keyword argument.
Every handler method receives every passed keyword argument meaning that you have to decide in the handler itself which
arguments you need. Use the ``**kwargs`` argument in this cases.

.. note::

    In the internal implementation when ``get_rows`` gets the model attribute it checks if it is a callable. If it's
    true then it is invoked with all keyword arguments of ``get_rows``. Otherwise no other processing is made and the
    value is stored in the row.

Stateful columns
----------------

It is possible to store column states in a persistent storage so you get back the same table when you reload the page.
Only column-related things are stored (order, ordering and if it's hidden). Current page and limit are not.

To make a resource columns stateful simply add the ``stateful`` to its meta class:

.. code-block:: python

        class StatefulColumns(YaatModelResource):
            class Meta:
                stateful = True

That's it. Any change is going to be saved in your database.

Stateful table pages
--------------------

Django-yaat can store yaat's last ``limit`` and ``offset`` values in the authenticated user's session so you can
send the exact same page every time the user arrives to the same table. This is useful for cases when the user
navigates away and back to the same table often.

Simply add the ``stateful_init`` to the meta class of the resource:

.. code-block:: python

        class StatefulInit(YaatModelResource):
            class Meta:
                stateful_init = True

You can combine this with ``stateful`` of course.