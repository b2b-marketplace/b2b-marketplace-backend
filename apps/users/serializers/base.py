from django.contrib.auth import get_user_model
from django.db import transaction
from djoser.conf import settings
from rest_framework import serializers

from apps.users.models import Address, PhoneNumber

User = get_user_model()


class BaseSerializer(serializers.ModelSerializer):
    """Абстрактный сериализатор для создания нового пользователя."""

    password = serializers.CharField(style={"input_type": "password"}, write_only=True)

    def perform_create(self, validated_data, **fields):
        """Создает пользователя."""
        with transaction.atomic():
            user = User.objects.create_user(**validated_data, **fields)
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user

    def _address_phone_attach(self, obj):
        """Создает объекты адреса и номера телефона."""
        address = obj.pop("address", None)
        phone_number = obj.pop("phone_number", None)

        address_obj = Address.objects.create(**address)
        phone_number_obj = PhoneNumber.objects.create(**phone_number)

        return {"address": address_obj, "phone_number": phone_number_obj}

    def _extract_relations(self, validated_data):
        """Извлекает один уровень вложенных отношений."""
        reverse_relations = {}
        for field_name, field in self.fields.items():
            if isinstance(field, serializers.ModelSerializer | serializers.ListSerializer):
                if field.source not in validated_data:
                    continue

                reverse_relations[field_name] = (
                    self.fields[field_name].Meta.model,
                    validated_data.pop(field_name),
                )
        return reverse_relations

    def update_or_create(self, validated_data):
        """Создает объекты компании или физ. лица."""
        reverse_relations = {}
        relations = self._extract_relations(validated_data)

        for field_name, (model, data) in relations.items():
            with transaction.atomic():
                address_phone = self._address_phone_attach(data)
                reverse_relations[field_name] = model.objects.create(**data, **address_phone)
        return reverse_relations
