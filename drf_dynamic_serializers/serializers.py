from abc import ABC

from rest_framework.serializers import Serializer, ModelSerializer

from .mixins import DynamicFieldsSerializerMixin

__all__ = ("DynamicFieldsSerializer", "DynamicFieldsModelSerializer")


class DynamicFieldsSerializer(DynamicFieldsSerializerMixin, Serializer):
    """
    Serializer with dynamic fields.
    """

    pass


class DynamicFieldsModelSerializer(DynamicFieldsSerializerMixin, ModelSerializer):
    """
    Model serializer with dynamic fields.
    """

    pass
