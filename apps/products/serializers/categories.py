from rest_framework import serializers

from apps.products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(read_only=True, source="parent")

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "parent_id")
