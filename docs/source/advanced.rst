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

Customizing the column foreign key
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Yaat's Column model has a foreign key to ``settings.AUTH_USER_MODEL`` by default. This is what you need in 99.9% of cases.
However sometimes you may want the columns to be accessible from a different model (like from a related model of the User class).

To adjust this set the ``settings.YAAT_FOREIGN_KEY`` key to a string. It is expected to be a dotted pair of the Django app
and the Django model just like for ``AUTH_USER_MODEL``. See the
`docs <https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#substituting-a-custom-user-model>`_.

After changing the foreign key you also have to set the ``settings.YAAT_REQUEST_ATTR`` setting because subclasses of
``YaatModelResource`` depend on ``request.user`` which is likely not an instance of the new foreign key class anymore.
This value is expected to be a single string. The attribute with the same name must exist in the ``request`` object.

Real world example
""""""""""""""""""

Let's say we have 2 models, ``Customer`` and ``User`` in an N:M relation through an other model, ``Membership``, similar to
the `Django example <https://docs.djangoproject.com/en/1.8/topics/db/models/#extra-fields-on-many-to-many-relationships>`_
example.

Here the same user should have different column lists depending on which of its membership is active. This means that
``columns`` should be a property of ``Membership`` instances. To achieve this set the setting:

.. code-block:: python

    YAAT_FOREIGN_KEY = 'myapp.Membership'

(Assume ``Membership`` model is in the ``myapp`` Django application)

Since ``Column.user`` is expected to point to a ``Membership`` instance, and ``request.user`` is still a ``User``, you
have to add the active ``Membership`` object to each request. It's the easiest using a middleware. Say the ``Membership``
is accessible through ``request.member`` then set the setting to this:

.. code-block:: python

    YAAT_REQUEST_ATTR = 'member'


.. note::
    Keep in mind that the name of the property ``Column.user`` stays the same if you override ``YAAT_FOREIGN_KEY``
    but it points to a different type of object then.

.. warning::

    Changing ``YAAT_FOREIGN_KEY`` has a huge impact just like changing ``AUTH_USER_MODEL``. Be sure to set this value
    before applying your migrations the very first time. If you set this value later the real foreign key in your
    database will still point to the old table.

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


Utility methods
---------------

There are a few utility methods that may help you in some rare cases.

.. py:class:: YaatModelResource

    .. py:classmethod:: invalidate_column_cache(user)

        This method forces to invalidate the given user's ``Column``. This can help you
        if you add a new ``Column`` object on the fly and you want to show it immediately.

        Argument ``user`` is expected to be an instance of ``AUTH_USER_MODEL`` class or
        ``YAAT_FOREIGN_KEY`` class if that's specified.

.. py:class:: YaatValidatorForm

    .. py:method:: invalidate_state()

        Every ``YaatModelResource`` (and its subclasses) gets the attribute ``self.validator_form`` when
        the ``YaatModelResource.common(request, *args, **kwargs)`` method is invoked. This form is used
        for validating the received data during paging but also for creating the initial data. If you
        set the resource meta to ``stateful_init = True`` the form keeps its last received data as the
        initialization state. If you'd like to drop this state call this method.