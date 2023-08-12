from rest_framework import viewsets

from apps.products import serializers
from apps.products.models import Product


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
