from typing import Any, Type, Callable

from rest_framework.serializers import Serializer

__all__ = ("DynamicFieldsSerializerMixinTestCase",)


class DynamicFieldsSerializerMixinTestCase:

    foo: Any
    bar: Any

    serializer_class_bar: Type[Serializer]
    serializer_class_foo: Type[Serializer]

    assertEqual: Callable
    assertTrue: Callable
    assertFalse: Callable

    def test_included_fields_root(self):
        serializer = self.serializer_class_bar(self.bar, included_fields=["boolean"])

        self.assertEqual(serializer.data, {"boolean": True})

    def test_included_fields_nested(self):
        serializer = self.serializer_class_bar(self.bar, included_fields=["foo.char"])

        self.assertEqual(serializer.data, {"foo": {"char": "a"}})

    def test_excluded_fields_root(self):
        serializer = self.serializer_class_bar(self.bar, excluded_fields=["boolean"])

        self.assertEqual(serializer.data, {"foo": {"char": "a", "integer": 1}})

    def test_excluded_fields_nested(self):
        serializer = self.serializer_class_bar(self.bar, excluded_fields=["foo.integer"])

        self.assertEqual(serializer.data, {"foo": {"char": "a"}, "boolean": True})

    def test_required_fields(self):
        serializer = self.serializer_class_foo(data={}, required_fields=[])

        self.assertTrue(serializer.is_valid(raise_exception=False))

    def test_non_nullable_fields(self):
        serializer = self.serializer_class_foo(data={'char': None, 'integer': None}, non_nullable_fields=[])

        self.assertTrue(serializer.is_valid(raise_exception=False))

    def test_default_required(self):
        serializer = self.serializer_class_foo(data={})

        self.assertFalse(serializer.is_valid(raise_exception=False))
        self.assertEqual(serializer.errors, {
            "char": ["This field is required."],
            "integer": ["This field is required."],
        })

    def test_default_non_nullable(self):
        serializer = self.serializer_class_foo(data={'char': None, 'integer': None})

        self.assertFalse(serializer.is_valid(raise_exception=False))
        self.assertEqual(serializer.errors, {
            "char": ["This field may not be null."],
            "integer": ["This field may not be null."],
        })