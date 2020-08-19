
drf-dynamic-serializers
=======================

.. image:: https://img.shields.io/github/stars/csdenboer/drf-dynamic-serializers.svg?label=Stars&style=socialcA
   :target: https://github.com/csdenboer/drf-dynamic-serializers
   :alt: GitHub

.. image:: https://img.shields.io/pypi/v/drf-dynamic-serializers.svg
   :target: https://pypi.org/project/drf-dynamic-serializers/
   :alt: PyPI release

.. image:: https://img.shields.io/readthedocs/drf-dynamic-serializers.svg
   :target: https://drf-dynamic-serializers.readthedocs.io/
   :alt: Documentation

Dynamic serializers and view(set)s for the Django REST Framework.

Functionality
-------------
DRF Dynamic Serializers is a package that aims to increase the reusability of Django REST Framework's serializer classes. Serializers that inherit from `DynamicFieldsSerializer` are dynamic. The fields to include and/or exclude can be overriden as well as the `allow_null` and `required` property of fields. A common use case is a list and a detail endpoint sharing the same serializer class but with different fields included.

Furthermore, the package provides a viewset class (`DynamicFieldsModelViewSet`) that extends Django REST Framework's ModelViewSet with the the ability to dynamically select the fields to include or exclude in a response by reading the `fields` and `omit` query parameters of a request.

Documentation
-------------

For more information on installation and configuration see the documentation at:

https://drf-dynamic-serializers.readthedocs.io/


Issues
------

If you have questions or have trouble using the app please file a bug report at:

https://github.com/csdenboer/drf-dynamic-serializers/issues


Contributions
-------------

It is best to separate proposed changes and PRs into small, distinct patches
by type so that they can be merged faster into upstream and released quicker:

* features,
* bugfixes,
* code style improvements, and
* documentation improvements.

All contributions are required to pass the quality gates configured
with the CI. This includes running tests and linters successfully
on the currently officially supported Python and Django versions.

The test automation is run automatically by Travis CI, but you can
run it locally with the ``tox`` command before pushing commits.