from rest_framework.viewsets import ModelViewSet

from .mixins import DynamicFieldsViewMixin

__all__ = ("DynamicFieldsModelViewSet",)


class DynamicFieldsModelViewSet(DynamicFieldsViewMixin, ModelViewSet):
    """
    Viewset with dynamic fields.
    """

    pass
