from django.contrib.auth import get_user_model
from rest_framework import serializers
from serializers.basketproducts import (
    BasketProductReadSerializer,
    BasketProductWriteSerializer,
)

from apps.baskets.models import Basket

User = get_user_model()


class BasketReadSerializer(serializers.ModelSerializer):
    """Сериализатор модели Basket, используемый при чтении корзины.

    Для вычисления значения basket_products происходит обращение к данным
    промежуточной модели.

    """

    # TODO: заменить на кастомный сериализатор пользователя
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    basket_products = BasketProductReadSerializer(
        read_only=True, many=True, source="basketproduct_set"
    )

    class Meta:
        model = Basket
        fields = "__all__"


class BasketWriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели Basket.

    Используется при записи объектов.
    """

    # TODO: заменить на кастомный сериализатор пользователя
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    basket_products = BasketProductWriteSerializer(many=True)

    class Meta:
        model = Basket
        fields = "__all__"
