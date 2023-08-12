from rest_framework import serializers

from apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "user",
            "category",
            "sku",
            "name",
            "brand",
            "price",
            "wholesale_quantity",
            "video",
            "quantity_in_stock",
            "description",
            "manufacturer_country",
        )
