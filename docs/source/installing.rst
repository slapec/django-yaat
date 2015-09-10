Installing
==========

1.  **The module is not on PyPI yet** but once it is published you can install it with ``pip`` like everything else:

    ::

        pip install django-yaat

2.  Then add the ``'yaat'`` module to the ``INSTALLED_APPS``.

3.  Migrate the models:

    ::

        python manage.py migrate yaat

