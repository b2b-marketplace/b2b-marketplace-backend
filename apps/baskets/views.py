from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.baskets.models import Basket
from apps.baskets.serializers.baskets import (
    BasketCreateSerializer,
    BasketReadSerializer,
    BasketWriteSerializer,
)


class BasketViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return Basket.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return BasketCreateSerializer
        if self.request.method in permissions.SAFE_METHODS:
            return BasketReadSerializer
        return BasketWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(exclude=True)
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(exclude=True)
    def partial_update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=False,
        methods=["get", "post", "put"],
        url_path="mine",
        serializer_class=BasketWriteSerializer,
    )
    def mine_basket(self, request):
        if request.method == "POST":
            serializer = self.get_serializer(data=request.data, context={"request": request})
        else:
            basket = Basket.objects.get(user=self.request.user)
            serializer = self.get_serializer(instance=basket, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
