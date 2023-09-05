from rest_framework import serializers

from apps.products.models import Image, Product
from apps.products.serializers import CategorySerializer, ImageSerializer
from apps.users.serializers.companies import (
    CompanyMiniFieldSerializer,
    CompanyReadSerializer,
)


class ProductReadSerializer(serializers.ModelSerializer):
    """Сериализатор для получения и отображения данных о товаре.

    Используется в безопасных http-методах.
    """

    images = ImageSerializer(many=True)
    category = CategorySerializer()
    seller = CompanyReadSerializer(read_only=True, source="user.company")
    is_favorited = serializers.BooleanField(default=False)

    class Meta:
        model = Product
        depth = 1
        fields = (
            "id",
            "seller",
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
            "images",
            "is_favorited",
        )


class ProductWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания нового товара или изменения существующего товара."""

    images = serializers.ListField(child=serializers.ImageField(), max_length=5, required=True)

    class Meta:
        model = Product
        fields = (
            "category",
            "sku",
            "name",
            "brand",
            "price",
            "wholesale_quantity",
            "quantity_in_stock",
            "description",
            "manufacturer_country",
            "video",
            "images",
        )

    def create_or_update_product(self, validated_data, instance=None):
        """Создаёт или обновляет товар.

        Аргументы:
            instance (Product | None): экземпляр модели товара. При передачи аргумента
        осуществляется обновление экземпляра. В противном случае - создание.
        """
        product = instance if instance else Product()
        image_list = validated_data.pop("images", None)
        for key, val in validated_data.items():
            setattr(product, key, val)
        product.save()
        if image_list:
            product.images.all().delete()
            for image in image_list:
                Image.objects.create(product=product, image=image)
        return product

    def create(self, validated_data):
        return self.create_or_update_product(validated_data)

    def update(self, instance, validated_data):
        return self.create_or_update_product(validated_data, instance=instance)

    def to_representation(self, instance):
        serializer = ProductReadSerializer(instance)
        return serializer.data


class ProductReadMiniFieldSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения ограниченного количества данных о товаре."""

    supplier = CompanyMiniFieldSerializer(source="user.company")
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "supplier", "sku", "name", "price", "image")

    def get_image(self, product):
        # TODO: оптимизировать запрос к Images.
        image = product.images.first()
        request = self.context.get("request")
        if image and request:
            return request.build_absolute_uri(image.image.url)
