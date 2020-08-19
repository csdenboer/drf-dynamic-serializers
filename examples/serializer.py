class PaymentSerializer(DynamicFieldsModelSerializer):
    id = serializers.IntegerField(allow_null=False, required=True)
    mutation = MutationSerializer()

    class Meta:
        model = Payment
        fields = "__all__"