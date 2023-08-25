from rest_framework import exceptions, permissions, viewsets

from apps.orders.models import Order
from apps.orders.permissions import IsOwner
from apps.orders.serializers.orders import OrderReadSerializer, OrderWriteSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwner]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        if self.request.user.id != int(self.kwargs["user_id"]):
            raise exceptions.PermissionDenied
        return Order.objects.get_related_queryset(self.request.user)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return OrderReadSerializer
        return OrderWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
