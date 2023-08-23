from rest_framework import serializers

from apps.orders.models import OrderProduct
from apps.products.serializers.products import ProductReadMiniFieldSerializer


class OrderProductReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения промежуточной модели."""

    product = ProductReadMiniFieldSerializer()

    class Meta:
        model = OrderProduct
        fields = ("product", "quantity", "discount")
