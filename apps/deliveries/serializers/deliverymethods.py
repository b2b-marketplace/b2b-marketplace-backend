from rest_framework import serializers

from apps.deliveries.models import DeliveryMethod


class DeliveryMethodReadSerializer(serializers.ModelSerializer):
    """Методы доставки."""

    class Meta:
        model = DeliveryMethod
        fields = ("id", "name", "description", "slug", "price")
