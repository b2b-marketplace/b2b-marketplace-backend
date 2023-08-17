from rest_framework import permissions, viewsets

from apps.baskets.models import Basket

# , BasketProduct, Product
from apps.baskets.serializers.baskets import BasketReadSerializer, BasketWriteSerializer

# from apps.baskets.serializers.basketproducts import BasketProductWriteSerializer
from apps.users.models import CustomUser

# from rest_framework.decorators import action
# from rest_framework.response import Response


class BasketViewSet(viewsets.ModelViewSet):
    # http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        user = CustomUser.objects.get(id=1)
        return Basket.objects.filter(user=user)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return BasketReadSerializer
        return BasketWriteSerializer

    def perform_create(self, serializer):
        user = CustomUser.objects.get(id=1)
        serializer.save(user=user)
