from rest_framework import serializers

from apps.orders.models import OrderProduct
from apps.products.models import Product
from apps.products.serializers.products import ProductReadMiniFieldSerializer


class OrderProductReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения промежуточной модели."""

    product = ProductReadMiniFieldSerializer().setup_eager_loading(Product.objects.all())

    class Meta:
        model = OrderProduct
        fields = ("product", "quantity", "discount", "cost", "cost_with_discount")


class OrderProductWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи промежуточной модели."""

    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderProduct
        fields = ("product", "quantity")
