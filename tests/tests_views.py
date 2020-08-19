from django.test import TestCase, override_settings
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory

from drf_dynamic_serializers.conf import DynamicFieldsConfig
from drf_dynamic_serializers.exceptions import SerializerDoesNotSupportDynamicFields
from drf_dynamic_serializers.serializers import DynamicFieldsSerializer
from drf_dynamic_serializers.views import DynamicFieldsModelViewSet

factory = APIRequestFactory()


class DynamicFieldsModelViewSetTestCase(TestCase):

    def setUp(self) -> None:
        class Serializer(DynamicFieldsSerializer):
            char = serializers.CharField(allow_null=False, required=True)

        class ViewSet(DynamicFieldsModelViewSet):
            serializer_class = Serializer
            request = Request(factory.get('/'))
            format_kwarg = None

        self.viewset = ViewSet()

    def test_non_dynamic_fields_serializer_class(self):
        class Serializer(serializers.Serializer):
            pass

        self.viewset.serializer_class = Serializer

        with self.assertRaises(SerializerDoesNotSupportDynamicFields):
            self.viewset.get_serializer()

    @override_settings(DRF_DYNAMIC_SERIALIZERS_QUERY_PARAM_INCLUDED_FIELDS="fields")
    def test_query_param_included_fields(self):
        self.viewset.request = Request(factory.get('/', data={"fields": "char"}))

        serializer = self.viewset.get_serializer()

        self.assertEqual(type(serializer), self.viewset.serializer_class)
        self.assertEqual(serializer._df_conf, DynamicFieldsConfig(
            included_fields=['char']
        ))

    @override_settings(DRF_DYNAMIC_SERIALIZERS_QUERY_PARAM_EXCLUDED_FIELDS="exclude")
    def test_query_param_excluded_fields(self):
        self.viewset.request = Request(factory.get('/', data={"exclude": "char"}))

        serializer = self.viewset.get_serializer()

        self.assertEqual(type(serializer), self.viewset.serializer_class)
        self.assertEqual(serializer._df_conf, DynamicFieldsConfig(
            excluded_fields=['char']
        ))

    def test_default_included_fields(self):
        self.viewset.default_included_fields = ["char"]

        serializer = self.viewset.get_serializer()

        self.assertEqual(type(serializer), self.viewset.serializer_class)
        self.assertEqual(serializer._df_conf, DynamicFieldsConfig(
            included_fields=['char']
        ))

    def test_default_excluded_fields(self):
        self.viewset.default_excluded_fields = ["char"]

        serializer = self.viewset.get_serializer()

        self.assertEqual(type(serializer), self.viewset.serializer_class)
        self.assertEqual(serializer._df_conf, DynamicFieldsConfig(
            excluded_fields=['char']
        ))

    def test_none(self):
        serializer = self.viewset.get_serializer()

        self.assertEqual(type(serializer), self.viewset.serializer_class)
        self.assertEqual(serializer._df_conf, DynamicFieldsConfig())

    def test_request_non_get(self):
        self.viewset.default_excluded_fields = ["char"]

        self.viewset.request = Request(factory.post('/'))

        serializer = self.viewset.get_serializer()

        self.assertEqual(type(serializer), self.viewset.serializer_class)
        self.assertEqual(serializer._df_conf, DynamicFieldsConfig())
