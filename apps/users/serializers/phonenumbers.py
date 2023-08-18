from rest_framework import serializers

from apps.users.models import PhoneNumber


class PhoneNumberSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных о номере телефона."""

    class Meta:
        model = PhoneNumber
        fields = ("id", "phone_number")
