from rest_framework import serializers

from apps.products.models import Image, Product, Video
from apps.products.serializers import CategorySerializer, ImageSerializer
from apps.products.serializers.videos import VideoSerializer
from apps.products.validators import validate_video
from apps.users.serializers.companies import (
    CompanyMiniFieldSerializer,
    CompanyReadSerializer,
)


class ProductReadSerializer(serializers.ModelSerializer):
    """Сериализатор для получения и отображения данных о товаре.

    Используется в безопасных http-методах.
    """

    images = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)

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
            "videos",
            "quantity_in_stock",
            "description",
            "manufacturer_country",
            "images",
            "is_favorited",
        )


class ProductWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создания нового товара или изменения существующего товара."""

    images = serializers.ListField(child=serializers.ImageField(), max_length=5, required=False)
    videos = serializers.ListField(
        child=serializers.FileField(validators=[validate_video]), max_length=1, required=False
    )

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
            "videos",
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
        video_list = validated_data.pop("videos", None)
        for key, val in validated_data.items():
            setattr(product, key, val)
        product.save()
        if image_list:
            product.images.all().delete()
            for image in image_list:
                Image.objects.create(product=product, image=image)
        if video_list:
            product.videos.all().delete()
            for video in video_list:
                Video.objects.create(product=product, video=video)
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
        fields = ("id", "supplier", "sku", "name", "image")

    def get_image(self, product):
        images = product.images.all()
        request = self.context.get("request")
        if images and request:
            return request.build_absolute_uri(images[0].image.url)
