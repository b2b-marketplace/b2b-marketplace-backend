from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.baskets.models import Basket
from apps.orders.models import Order
from apps.orders.serializers.orderproducts import (
    OrderProductReadSerializer,
    OrderProductWriteSerializer,
)


class OrderReadSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения заказов в личном кабинете покупателя."""

    order_products = OrderProductReadSerializer(many=True, source="orders")

    class Meta:
        model = Order
        fields = ("id", "user", "status", "created_at", "order_products")


class OrderWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания заказов покупателем."""

    order_products = OrderProductWriteSerializer(many=True)

    class Meta:
        model = Order
        fields = ("order_products",)

    def validate(self, attrs):
        for order_product in attrs["order_products"]:
            product = order_product["product"]
            if order_product["quantity"] < 0:
                raise serializers.ValidationError(_("Item quantity must be greater than zero"))

            if product.quantity_in_stock < order_product["quantity"]:
                raise serializers.ValidationError(_("Quantity to order cannot be more than stock"))

        return attrs

    def create_or_update_order(self, validated_data, instance=None):
        order_products = validated_data.pop("order_products", None)
        order = instance if instance else Order()
        basket = Basket.objects.filter(user=validated_data["user"]).first()

        for key, value in validated_data.items():
            setattr(order, key, value)
        order.save()

        for order_product in order_products:
            product = order_product.pop("product")
            order.order_products.add(product, through_defaults=order_product)
            if basket:
                basket.basket_products.remove(product)

            # TODO: заменить на правильно считающую формулу обновления количества товара
            product.quantity_in_stock -= order_product.get("quantity", 0)
            product.save()

        return order

    @transaction.atomic
    def create(self, validated_data):
        return self.create_or_update_order(validated_data)

    def to_representation(self, instance):
        serializer = OrderReadSerializer(instance, context=self.context)
        return serializer.data
