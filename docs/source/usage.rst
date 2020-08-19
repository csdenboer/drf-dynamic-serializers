Usage
=======================

Serializer
--------------------

Serializers that inherit from DynamicFieldsSerializer can be configured using the following keyword arguments:

- ``included_fields``: list of field names to include in the serializer.
- ``excluded_fields``: list of field names to exclude from the serializer.
- ``required_fields``: list of field names that are required.
- ``non_nullable_fields``: list of field names that are non-nullable.

.. literalinclude:: ../../examples/serializer.py
  :language: Python

View
--------------------

.. literalinclude:: ../../examples/view.py
  :language: Python

Example URLs:

- ``/payments/?fields=id,mutation.delta``
- ``/payments/?exclude=id,mutation.delta``