from rest_framework import serializers

from apps.products.models import Video


class VideoSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных об видео."""

    class Meta:
        model = Video
        fields = ("video",)
