from rest_framework import mixins, parsers, permissions, viewsets

from apps.products import serializers
from apps.products.models import Category, Product
from apps.products.permissions import (
    IsOwnerOfProductOrReadOnly,
    IsSellerCompanyOrReadOnly,
)


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = serializers.ProductReadSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    permission_classes = (IsSellerCompanyOrReadOnly, IsOwnerOfProductOrReadOnly)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.ProductReadSerializer
        return serializers.ProductWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
