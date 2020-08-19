from collections import defaultdict
from typing import Callable, List, Tuple, Set

from django.utils.functional import cached_property
from rest_framework.serializers import ListSerializer, Serializer
from rest_framework.request import Request

from .conf import DynamicFieldsConfig, settings
from .exceptions import SerializerDoesNotSupportDynamicFields

__all__ = (
    "DynamicFieldsPolymorphicSerializerMixin",
    "DynamicFieldsSerializerMixin",
    "DynamicFieldsViewMixin",
)


class DynamicFieldsPolymorphicSerializerMixin:
    """
    Mixin that implements dynamic fields for PolymorphicSerializers (see
    https://github.com/apirobot/django-rest-polymorphic).
    """

    dynamic_fields = True

    _df_config: DynamicFieldsConfig
    to_resource_type: Callable

    def __init__(self, *args, **kwargs):
        # popup df related arguments, so that we will not get unexpected arguments error
        self._df_conf = DynamicFieldsConfig(
            included_fields=kwargs.pop("included_fields", None),
            excluded_fields=kwargs.pop("excluded_fields", None),
            required_fields=kwargs.pop("required_fields", None),
            non_nullable_fields=kwargs.pop("non_nullable_fields", None),
        )

        super().__init__(*args, **kwargs)

        model_serializer_mapping = self.model_serializer_mapping
        self.model_serializer_mapping = {}
        self.resource_type_model_mapping = {}

        for model, serializer in model_serializer_mapping.items():
            resource_type = self.to_resource_type(model)

            if callable(serializer):
                is_dynamic_fields_serializer = getattr(
                    serializer, "dynamic_fields", False
                )

                # pass df config to initialization of serializer
                serializer = serializer(
                    *args,
                    **(
                        {**kwargs, **self._df_conf.__dict__}
                        if is_dynamic_fields_serializer
                        else kwargs
                    )
                )
                serializer.parent = self

            self.resource_type_model_mapping[resource_type] = model
            self.model_serializer_mapping[model] = serializer

    def set_df_config(self, config: DynamicFieldsConfig) -> None:
        """
        Set config 'config' as dynamic fields config.
        """
        # loop over all serializers in this polymorphic's serializer and set config 'config' as dynamic fields config
        for model, serializer in self.model_serializer_mapping.items():
            if getattr(serializer, "dynamic_fields", False):
                serializer.set_df_config(config)


class DynamicFieldsSerializerMixin:
    """
    Mixin that adds the ability to dynamically configure a serializer's fields. Fields can be included and/or excluded
    and the 'required' and 'allow_null' properties of fields can be overridden.
    """

    dynamic_fields = True

    _df_config: DynamicFieldsConfig

    def __init__(self, *args, **kwargs):
        self._df_conf = DynamicFieldsConfig(
            included_fields=kwargs.pop("included_fields", None),
            excluded_fields=kwargs.pop("excluded_fields", None),
            required_fields=kwargs.pop("required_fields", None),
            non_nullable_fields=kwargs.pop("non_nullable_fields", None),
        )

        super().__init__(*args, **kwargs)

    @cached_property
    def fields(self) -> dict:
        """
        Get fields to serialize given the fields to include and fields to exclude.
        """
        fields = super(DynamicFieldsSerializerMixin, self).fields

        included_fields_root, included_fields_nested = self._split_levels(
            self._df_conf.included_fields or []
        )
        excluded_fields_root, excluded_fields_nested = self._split_levels(
            self._df_conf.excluded_fields or []
        )

        # if there are fields to clean
        if len(included_fields_root) != 0 or len(excluded_fields_root) != 0:
            self._clean_fields(
                fields,
                excluded_fields_root,
                included_fields_root,
                excluded_fields_nested,
            )

        # pass included and excluded fields to fields (used by nested serializers).
        for name, field in fields.items():
            self._set_df_conf_for_field(
                field,
                DynamicFieldsConfig(
                    included_fields=included_fields_nested.get(name, None),
                    excluded_fields=excluded_fields_nested.get(name, None),
                ),
            )
            # set dynamic properties, e.g. allow_null and required
            self._apply_dynamic_properties_for_field(fields, name)

        return fields

    def set_df_config(self, config: DynamicFieldsConfig):
        """
        Set config 'config' as dynamic fields config.
        """
        self._df_conf = config

    def _apply_dynamic_properties_for_field(self, fields, field_name) -> None:
        """
        Set dynamic properties to field with name 'field_name' in fields 'fields'.
        """
        # if we want to overwrite the 'required' property of the fields
        if self._df_conf.required_fields is not None:
            fields[field_name].required = field_name in self._df_conf.required_fields

        # if we want to overwrite the 'allow_null' property of the fields
        if self._df_conf.non_nullable_fields is not None:
            fields[field_name].allow_null = (
                field_name not in self._df_conf.non_nullable_fields
            )

    def _clean_fields(
        self,
        fields: dict,
        excluded_fields_root: Set[str],
        included_fields_root: Set[str],
        excluded_fields_nested: dict,
    ) -> None:
        """
        Clean fields 'fields' given excluded fields 'excluded_fields_root', included fields 'included_fields_root' and
        nested excluded fields 'excluded_fields_nested'.
        """
        to_remove = []

        for field_name in fields:
            is_included = self._is_field_included(
                field_name,
                excluded_fields_root,
                included_fields_root,
                excluded_fields_nested,
            )

            if not is_included:
                # we cannot pop while iterating
                to_remove.append(field_name)

        for remove_field in to_remove:
            fields.pop(remove_field)

    @staticmethod
    def _is_field_included(
        field_name: str,
        excluded_fields: Set[str],
        included_fields: Set[str],
        nested_excluded_fields: dict,
    ) -> bool:
        """
        Check whether field with name 'field_name' should exist (be serialized) given excluded fields
        'excluded_fields_root', included fields 'included_fields_root' and nested excluded fields
        'excluded_fields_nested'.
        """
        # We don't want to prematurely exclude a field, eg "exclude=house.rooms.kitchen" should not exclude the entire
        # house or all the rooms, just the kitchen.
        if field_name in excluded_fields and field_name not in nested_excluded_fields:
            return False

        # if included fields are set (filtering is enabled) and field is not in included_fields, then return False
        if len(included_fields) > 0 and field_name not in included_fields:
            return False

        return True

    @staticmethod
    def _split_levels(fields: List[str]) -> Tuple[set, defaultdict]:
        """
        Convert nested fields into current-level fields and next level fields.
        """
        first_level_fields = set()
        next_level_fields = defaultdict(list)

        for e in fields:
            if "." in e:
                # split on first .
                first_level, next_level = e.split(".", 1)
                first_level_fields.add(first_level)
                next_level_fields[first_level].append(next_level)
            else:
                first_level_fields.add(e)

        return first_level_fields, next_level_fields

    @staticmethod
    def _set_df_conf_for_field(field, df_config: DynamicFieldsConfig) -> None:
        """
        Set included fields 'included_fields' and excluded field 'fields' to field 'field'.
        """
        # if field has support for dynamic fields, then set df config
        if getattr(field, "dynamic_fields", False):
            field.set_df_config(df_config)
        elif type(field) == ListSerializer and getattr(
            field.child, "dynamic_fields", False
        ):
            field.child.set_df_config(df_config)


class DynamicFieldsViewMixin:
    """
    Mixin for view(set)s that adds the ability to dynamically select the fields to include or exclude in a response by
    reading the query parameters in the request.
    """
    default_included_fields: List[str]
    default_excluded_fields: List[str]

    request: Request

    get_serializer_class: Callable
    get_serializer_context: Callable

    def get_serializer(self, *args, **kwargs) -> Serializer:
        """
        Get serializer given the dynamically excluded and/or included fields.
        """
        serializer_class = self.get_serializer_class()

        if getattr(serializer_class, "dynamic_fields", False) is False:
            raise SerializerDoesNotSupportDynamicFields()

        kwargs["context"] = self.get_serializer_context()

        if self._is_eligible_for_dynamic_fields():
            kwargs["included_fields"] = self._get_included_fields()
            kwargs["excluded_fields"] = self._get_excluded_fields()

        return serializer_class(*args, **kwargs)

    def _get_included_fields(self) -> List[str]:
        """
        Get names of the fields to include.
        """
        return (
            self._parse_query_params_for_field(
                settings.DRF_DYNAMIC_SERIALIZERS_QUERY_PARAM_INCLUDED_FIELDS
            )
            or self._get_default_included_fields()
        )

    def _get_excluded_fields(self) -> List[str]:
        """
        Get names of the fields to exclude.
        """
        return (
            self._parse_query_params_for_field(
                settings.DRF_DYNAMIC_SERIALIZERS_QUERY_PARAM_EXCLUDED_FIELDS
            )
            or self._get_default_excluded_fields()
        )

    def _get_default_included_fields(self) -> List[str]:
        """
        Get names of the fields to include by default.
        """
        return getattr(self, "default_included_fields", None)

    def _get_default_excluded_fields(self) -> List[str]:
        """
        Get names of the fields to exclude by default.
        """
        return getattr(self, "default_excluded_fields", None)

    def _is_eligible_for_dynamic_fields(self) -> bool:
        """
        Verify whether the request is eligible for dynamic fields. This is the case if all of the following conditions
        are fulfilled:
        - request method is GET
        """
        return self.request is not None and self.request.method == "GET"

    def _parse_query_params_for_field(self, field: str) -> List[str]:
        """
        Get parsed value of query params for field 'field'.
        """
        value = self.request.query_params.get(field)
        return value.split(",") if value else None
