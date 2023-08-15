# from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.baskets.models import Basket

from .basketproducts import BasketProductReadSerializer

# , BasketProduct

# , BasketProductWriteSerializer

# User = get_user_model()


class BasketReadSerializer(serializers.ModelSerializer):
    """Сериализатор модели Basket. Используется при чтении корзины.

    Для вычисления значения basket_products происходит обращение к данным
    промежуточной модели.

    """

    # TODO: заменить на кастомный сериализатор пользователя
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    basket_products = BasketProductReadSerializer(read_only=True, many=True, source="basket")

    class Meta:
        model = Basket
        fields = ("id", "user", "basket_products")


class BasketWriteSerializer(serializers.ModelSerializer):
    """Сериализатор модели Basket.

    Используется для создания корзины.
    """

    # TODO: заменить на кастомный сериализатор пользователя
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    # basket_products = BasketProductWriteSerializer(many=True)

    class Meta:
        model = Basket
        fields = "__all__"

    # def create_products_quantity(self, basket_products, basket):
    #     for product in basket_products:
    #         BasketProduct.objects.create(
    #             basket=basket,
    #             product_id=product['id'],
    #             quantity=product['quantity'])

    # def create(self, validated_data):
    #     basket_products = validated_data.pop('basket_products')
    #     basket = Basket.objects.create(**validated_data)
    #     self.create_products_quantity(basket_products, basket)
    #     return basket

    # def update(self, basket, validated_data):
    #     basket_products = validated_data.pop('basket_products')
    #     basket.basket_products.clear()
    #     self.create_products_quantity(basket_products, basket)
    #     return super().update(basket, validated_data)

    # def to_representation(self, basket):
    #     representation = BasketReadSerializer(
    #         basket, context={'request': self.context.get('request')})
    #     return representation.data
