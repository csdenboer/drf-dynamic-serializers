Installation
=======================

DRF Dynamic Serializers is easy to install from the PyPI index:

.. code-block:: bash

   $ pip install drf-dynamic-serializers

This will install ``drf-dynamic-serializers`` along with its dependencies:

* django;
* django-rest-framework;
* django-appconf.

After installing the package, the project settings need to be configured.

Add ``drf_dynamic_serializers`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # DRF Dynamic Serializers app can be in any position in the INSTALLED_APPS list.
        'drf_dynamic_serializers',
    ]