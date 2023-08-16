from rest_framework import serializers

from apps.users.models import Address


class AddressSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных оо адресе."""

    class Meta:
        model = Address
        fields = ("id", "address")
