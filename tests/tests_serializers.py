from django.db import models
from django.test import TestCase
from rest_framework import serializers

from drf_dynamic_serializers.serializers import DynamicFieldsSerializer, DynamicFieldsModelSerializer
from tests.tests_mixins import DynamicFieldsSerializerMixinTestCase


class FooSerializer(DynamicFieldsSerializer):
    char = serializers.CharField(allow_null=False, required=True)
    integer = serializers.IntegerField(allow_null=False, required=True)


class BarSerializer(DynamicFieldsSerializer):
    boolean = serializers.BooleanField(allow_null=False, required=True)
    foo = FooSerializer()


class Foo:

    char: str
    integer: int

    def __init__(self, char: str, integer: int):
        self.char = char
        self.integer = integer


class Bar:

    boolean: bool
    foo: Foo

    def __init__(self, boolean: bool, foo: Foo):
        self.boolean = boolean
        self.foo = foo


class DynamicFieldsSerializerTestCase(DynamicFieldsSerializerMixinTestCase, TestCase):

    serializer_class_bar = BarSerializer
    serializer_class_foo = FooSerializer

    def setUp(self) -> None:
        self.foo = Foo(char="a", integer=1)
        self.bar = Bar(boolean=True, foo=self.foo)


class FooModel(models.Model):

    char = models.CharField(max_length=10)
    integer = models.IntegerField()

    class Meta:
        app_label = "tests"


class BarModel(models.Model):

    boolean = models.BooleanField()
    foo = models.ForeignKey(FooModel, on_delete=models.CASCADE)

    class Meta:
        app_label = "tests"


class FooModelSerializer(DynamicFieldsModelSerializer):
    char = serializers.CharField(allow_null=False, required=True)
    integer = serializers.IntegerField(allow_null=False, required=True)

    class Meta:
        model = FooModel
        fields = "__all__"


class BarModelSerializer(DynamicFieldsModelSerializer):
    boolean = serializers.BooleanField(allow_null=False, required=True)
    foo = FooSerializer()

    class Meta:
        model = BarModel
        fields = "__all__"


class DynamicFieldsModelSerializerTestCase(DynamicFieldsSerializerMixinTestCase, TestCase):

    serializer_class_bar = BarModelSerializer
    serializer_class_foo = FooModelSerializer

    def setUp(self) -> None:
        self.foo = Foo(char="a", integer=1)
        self.bar = Bar(boolean=True, foo=self.foo)
