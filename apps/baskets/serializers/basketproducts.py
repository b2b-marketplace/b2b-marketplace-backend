from rest_framework import serializers

from apps.baskets.models import BasketProduct
from apps.products.models import Product


class BasketProductReadSerializer(serializers.ModelSerializer):
    """Сериализатор промежуточной модели BasketProduct.

    Для чтения корзины.
    """

    id = serializers.IntegerField(source="product.id", read_only=True)

    class Meta:
        model = BasketProduct
        fields = ("id", "quantity")


class BasketProductWriteSerializer(serializers.ModelSerializer):
    """Сериализатор промежуточной модели BasketProduct.

    Для записи корзины.
    """

    id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ("id", "quantity")
