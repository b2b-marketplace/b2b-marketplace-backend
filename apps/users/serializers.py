from django.contrib.auth import get_user_model
from django.db import transaction
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from apps.users.models import Address, Company, PhoneNumber

User = get_user_model()


class PhoneNumberSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных о номере телефона."""

    class Meta:
        model = PhoneNumber
        fields = ("id", "phone_number")


class AddressSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных оо адресе."""

    class Meta:
        model = Address
        fields = ("id", "address")


class AddressPhoneSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    phone_number = PhoneNumberSerializer()

    class Meta:
        abstract = True


class CompanySerializer(AddressPhoneSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class BaseSerializer(UserCreateSerializer):
    class Meta:
        model = User

    def validate(self, attrs):
        return attrs

    def perform_create(self, validated_data, **kwargs):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data, **kwargs)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user

    def _address_phone_attach(self, obj):
        address = obj.pop("address", None)
        phone_number = obj.pop("phone_number", None)

        address_obj = Address.objects.create(**address)
        phone_number_obj = PhoneNumber.objects.create(**phone_number)

        return {"address": address_obj, "phone_number": phone_number_obj}

    def _extract_relations(self, validated_data):
        reverse_relations = {}
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.ModelSerializer):
                if field.source not in validated_data:
                    continue

                reverse_relations[field_name] = (
                    self.fields[field_name].Meta.model,
                    validated_data.pop(field_name),
                )
        return reverse_relations

    def update_or_create(self, validated_data):
        reverse_relations = {}
        relations = self._extract_relations(validated_data)

        for field_name, (model, data) in relations.items():
            with transaction.atomic():
                address_phone = self._address_phone_attach(data)
                reverse_relations[field_name] = model.objects.create(**data, **address_phone)
        return reverse_relations


class CompanyCreateSerializer(BaseSerializer):
    company = CompanySerializer()

    class Meta(BaseSerializer.Meta):
        fields = ("id", "email", "username", "is_company", "company", "password")

    @transaction.atomic
    def create(self, validated_data):
        relations = self.update_or_create(validated_data)
        return self.perform_create(validated_data, **relations, is_company=True)
