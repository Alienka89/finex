from rest_framework import serializers

from currency.models import Currency, Rate


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ("id", "name")


class RateSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer(many=False, read_only=True)

    class Meta:
        model = Rate
        fields = ("id", "date", "rate", "volume")


class LastRateSerializer(serializers.Serializer):
    rate = serializers.FloatField()
    volume = serializers.FloatField()

    class Meta:
        fields = ("rate", "volume",)


class OneRateSerializer(serializers.Serializer):
    average_volume = serializers.FloatField(required=False)
    last_rate = LastRateSerializer(many=False, read_only=True, required=False)
    success = serializers.BooleanField(required=True)
    currency = serializers.CharField(required=False)

    class Meta:
        fields = ("success", "average_volume", "last_rate", "currency")
