from collections import defaultdict

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

    def _sort_products_by_sellers(self, order_products):
        sorting_products = defaultdict(list)
        for order_product in order_products:
            product = order_product.get("product")
            seller = product.user
            sorting_products[seller].append(order_product)
        return sorting_products

    def _save_obj(self, obj_model, data):
        for key, value in data.items():
            setattr(obj_model, key, value)
        obj_model.save()

    def create_or_update_order(self, validated_data, instance=None):
        order_products = validated_data.pop("order_products", None)
        sorting_products = self._sort_products_by_sellers(order_products)
        basket = Basket.objects.filter(user=validated_data["user"]).first()
        orders = []

        for sorting_product in sorting_products.values():
            order = instance if instance else Order()
            self._save_obj(order, validated_data)

            for products in sorting_product:
                product = products.pop("product")
                products["price"] = product.price
                order.order_products.add(product, through_defaults=products)

                if basket:
                    basket.basket_products.remove(product)

                # TODO: заменить на правильно считающую формулу обновления количества товара
                product.quantity_in_stock -= products.get("quantity", 0)
                product.save()

            orders.append(order)

        return orders

    @transaction.atomic
    def create(self, validated_data):
        return self.create_or_update_order(validated_data)

    def to_representation(self, instance):
        serializer = OrderReadSerializer(instance, context=self.context, many=True)
        return serializer.data
