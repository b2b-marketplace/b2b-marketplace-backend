from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from apps.users.models import Company
from apps.users.serializers.addresses import AddressSerializer
from apps.users.serializers.phonenumbers import PhoneNumberSerializer

User = get_user_model()


class CompanyReadSerializer(serializers.ModelSerializer):
    """Сериализатор для получения и отображения публичных данных о компании.

    Используется в безопасных http-методах.
    """

    address = AddressSerializer(read_only=True)
    phone_number = PhoneNumberSerializer(read_only=True)

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
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
            "ogrn",
            "company_account",
            "phone_number",
            "address",
        )

    def to_representation(self, instance):
        serializer = CompanyReadSerializer(instance)
        return serializer.data


class UserCompanyReadSerializer(serializers.ModelSerializer):
    """Сериализатор для получения и отображения публичных данных о пользователях-компаниях.

    Используется в безопасных http-методах.
    """

    company = CompanyReadSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "is_company",
            "company",
        )


class UserCompanyWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания пользователя-компании."""

    password = serializers.CharField(style={"input_type": "password"}, write_only=True)
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
        return User.objects.create_user(**validated_data)

    def to_representation(self, instance):
        serializer = UserCompanyReadSerializer(instance)
        return serializer.data


class MeUserCompanyReadSerializer(serializers.ModelSerializer):
    """Сериализатор для получения и отображения данных в личном кабинете о пользователях-компаниях.

    Используется в безопасных http-методах.
    """

    class Meta:
        model = User
        depth = 2
        fields = (
            "id",
            "email",
            "username",
            "is_company",
            "company",
        )


class MeUserCompanyWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления данных в личном кабинете."""

    company = CompanyWriteSerializer()

    class Meta:
        model = User
        fields = ("company",)

    @transaction.atomic
    def update(self, instance, validated_data):
        return User.objects.update_user(instance, validated_data)

    def to_representation(self, instance):
        serializer = MeUserCompanyReadSerializer(instance)
        return serializer.data
