from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.baskets.models import Basket
from apps.baskets.serializers.baskets import (
    BasketCreateSerializer,
    BasketReadSerializer,
    BasketWriteSerializer,
)
from apps.users.models import CustomUser


class BasketViewSet(viewsets.ModelViewSet):
    # http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        user = CustomUser.objects.get(id=1)
        return Basket.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == "create":
            return BasketCreateSerializer
        if self.request.method in permissions.SAFE_METHODS:
            return BasketReadSerializer
        return BasketWriteSerializer

    def perform_create(self, serializer):
        user = CustomUser.objects.get(id=1)
        serializer.save(user=user)

    @action(detail=False, methods=["post"], url_path="mine", serializer_class=BasketWriteSerializer)
    def add_products_to_basket(self, request):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Products added to the basket successfully"})
