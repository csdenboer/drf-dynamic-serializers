from typing import Optional, List

# recommended by appconf package to import first
from django.conf import settings
from appconf import AppConf

__all__ = ("DynamicFieldsConfig",)


class DRFDynamicSerializersConf(AppConf):

    # query param to pass fields to include in response
    QUERY_PARAM_INCLUDED_FIELDS = "fields"
    # query param to pass fields to exclude from response
    QUERY_PARAM_EXCLUDED_FIELDS = "exclude"

    class Meta:
        prefix = "drf_dynamic_serializers"


class DynamicFieldsConfig:
    included_fields: Optional[List[str]]
    excluded_fields: Optional[List[str]]
    required_fields: Optional[List[str]]
    non_nullable_fields: Optional[List[str]]

    def __init__(
        self,
        included_fields: Optional[List[str]] = None,
        excluded_fields: Optional[List[str]] = None,
        required_fields: Optional[List[str]] = None,
        non_nullable_fields: Optional[List[str]] = None,
    ):
        self.included_fields = included_fields
        self.excluded_fields = excluded_fields
        self.required_fields = required_fields
        self.non_nullable_fields = non_nullable_fields

    def __eq__(self, other):
        return (
            type(self) == type(other)
            and self.included_fields == other.included_fields
            and self.excluded_fields == other.excluded_fields
            and self.required_fields == other.required_fields
            and self.non_nullable_fields == other.non_nullable_fields
        )
