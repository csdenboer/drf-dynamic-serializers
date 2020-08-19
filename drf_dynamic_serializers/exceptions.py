__all__ = ("DRFDynamicSerializersError", "SerializerDoesNotSupportDynamicFields")


class DRFDynamicSerializersError(Exception):
    """
    Base exception class for drf-dynamic-serializers exceptions.
    """

    pass


class SerializerDoesNotSupportDynamicFields(DRFDynamicSerializersError):
    """
    Raised when a view(set) with dynamic fields does not use a serializer class with dynamic fields.
    """

    pass
