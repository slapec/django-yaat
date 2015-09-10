Advanced resources
==================

Custom columns
--------------

In the meta class of the resource you can list either strings or ``Column`` objects under the ``columns`` property. String
keys must always match a field of the model. ``Column`` keys however are free to have any values. ``Column`` objects
have the property ``key`` which is going to be used for model property lookup. This is very useful to send values
of related models or computed values in the ``POST``.

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
                Column('get_owner', 'Owner'),
                'name', 'quantity', 'price',
                Column('get_total_price', 'Total price')
            )

First you have to import the ``Column`` model. ``Column`` objects are going to be mapped to the properties of model
of the resource by their key (the first argument). So in this example when the resource iterates over the queryset
it will get ``get_owner`` property of the model first, then ``name``, ``quantity``, ``prce`` fields of the model,
then ``get_total_price`` property of the model at the end.

We call these columns *virtual* meaning that you can't order by their values out of box (because the ORM can't handle
it).

However the ``Column`` class is a Django model but it's never stored in the database unless you mark the resource to be
stateful.