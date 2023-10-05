from rest_framework import serializers

from apps.deliveries.models import Delivery, DeliveryMethod
from apps.deliveries.serializers.deliverymethods import DeliveryMethodReadSerializer
from apps.users.models import Address
from apps.users.serializers.addresses import AddressSerializer


class DeliveryReadSerializer(serializers.ModelSerializer):
    """Отображение доставок."""

    address = AddressSerializer()
    delivery_method = DeliveryMethodReadSerializer()

    class Meta:
        model = Delivery
        fields = ("id", "address", "delivery_method", "delivery_date")


class DeliveryWriteSerializer(serializers.ModelSerializer):
    """Оформление доставки."""

    address = serializers.CharField()
    delivery_method = serializers.PrimaryKeyRelatedField(queryset=DeliveryMethod.objects.all())

    class Meta:
        model = Delivery
        fields = ("address", "delivery_method", "delivery_date")

    def validate(self, attrs):
        address_data = attrs["address"]
        address, _created = Address.objects.get_or_create(address=address_data)
        attrs["address"] = address
        return attrs
