from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from apps.users.models import Company
from apps.users.serializers.addresses import AddressSerializer
from apps.users.serializers.base import BaseSerializer
from apps.users.serializers.phonenumbers import PhoneNumberSerializer

User = get_user_model()


class CompanyReadSerializer(serializers.ModelSerializer):
    """Сериализатор для получения и отображения данных о компании.

    Используется в безопасных http-методах.
    """

    class Meta:
        model = Company
        depth = 1
        fields = (
            "id",
            "role",
            "name",
            "company_account",
            "inn",
            "ogrn",
            "phone_number",
            "address",
        )


class CompanyWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания компании."""

    address = AddressSerializer()
    phone_number = PhoneNumberSerializer()

    class Meta:
        model = Company
        fields = (
            "role",
            "name",
            "inn",
            "phone_number",
            "address",
        )

    def to_representation(self, instance):
        serializer = CompanyReadSerializer(instance)
        return serializer.data


class UserCompanyReadSerializer(serializers.ModelSerializer):
    """Сериализатор для получения и отображения данных о пользователях-компаниях.

    Используется в безопасных http-методах.
    """

    company = CompanyReadSerializer()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "is_company",
            "company",
        )


class UserCompanyWriteSerializer(BaseSerializer):
    """Сериализатор для создания пользователя-компании."""

    company = CompanyWriteSerializer()

    class Meta:
        model = User
        fields = (
            "email",
            "username",
            "password",
            "company",
        )

    @transaction.atomic
    def create(self, validated_data):
        relations = self.update_or_create(validated_data)
        return self.perform_create(validated_data, **relations, is_company=True)

    def to_representation(self, instance):
        serializer = UserCompanyReadSerializer(instance)
        return serializer.data
