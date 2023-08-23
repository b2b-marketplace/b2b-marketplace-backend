from rest_framework import serializers

from apps.orders.models import Order
from apps.orders.serializers.orderproducts import OrderProductReadSerializer


class OrderReadSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения заказов в личном кабинете покупателя."""

    order_products = OrderProductReadSerializer(many=True, source="orders")

    class Meta:
        model = Order
        fields = ("id", "user", "status", "created_at", "order_products")
