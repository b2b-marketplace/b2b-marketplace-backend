from rest_framework import serializers

from apps.products.models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",  # +
            "user",  # + ??? - юзер сериалайзер
            "category",  # + - посмотреть, категория выпадающая! ??? нужна ли она?
            "sku",  # + ???
            "name",  # +
            "brand",  # +
            "price",  # +
            "wholesale_quantity",  # +
            "video",  # video
            "quantity_in_stock",  # + ????
            "description",  # description
            "manufacturer_country",  # + ???
            # "images"  # IMAGES all
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий товаров."""

    parent_id = serializers.PrimaryKeyRelatedField(read_only=True, source="parent")

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent_id")
