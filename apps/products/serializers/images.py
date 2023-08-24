from rest_framework import serializers

from apps.products.models import Image


class ImageSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных об изображении."""

    class Meta:
        model = Image
        fields = ("image",)


class OneItemFromListSerializer(serializers.ListSerializer):
    """Отдает один объект из списка."""

    def to_representation(self, data):
        images = super().to_representation(data)
        return images[0]


class ImagePreviewSerializer(serializers.ModelSerializer):
    """Сериализатор для получения изображения товара."""

    class Meta:
        list_serializer_class = OneItemFromListSerializer
        model = Image
        fields = ("image",)
