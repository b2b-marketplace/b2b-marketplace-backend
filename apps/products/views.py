from django.db.models import Exists, OuterRef
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, parsers, permissions, viewsets

from apps.products import serializers
from apps.products.filters import CategoryFilter, ProductFilter
from apps.products.models import Category, Product
from apps.products.permissions import (
    IsOwnerOfProductOrReadOnly,
    IsSellerCompanyOrReadOnly,
)


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """Вьюсет для работы с категориями."""

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CategoryFilter


class ProductViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с продуктами."""

    serializer_class = serializers.ProductReadSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    permission_classes = (IsSellerCompanyOrReadOnly, IsOwnerOfProductOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = (
            Product.objects.all()
            .select_related(
                "user__company", "user__company__address", "user__company__phone_number"
            )
            .order_by("-id")
        )
        user = self.request.user
        if user.is_authenticated:
            return queryset.annotate(
                is_favorited=Exists(user.favorite_products.filter(product=OuterRef("id")))
            )
        return queryset

    def get_serializer_class(self):
        """Возвращает класс сериализатора."""
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.ProductReadSerializer
        return serializers.ProductWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
