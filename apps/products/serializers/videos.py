from rest_framework import serializers

from apps.products.models import Video
from apps.products.validators import validate_video


class VideoSerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных об видео."""

    default_validators = [validate_video]

    class Meta:
        model = Video
        fields = ("video",)
