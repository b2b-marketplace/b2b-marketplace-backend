from rest_framework import serializers

from apps.products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для получения данных о категории."""

    parent_id = serializers.PrimaryKeyRelatedField(read_only=True, source="parent")

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent_id")
