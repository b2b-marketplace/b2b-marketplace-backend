from rest_framework import permissions, viewsets

from apps.baskets.models import Basket
from apps.baskets.serializers.baskets import BasketReadSerializer, BasketWriteSerializer

# from apps.users.models import CustomUser


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all().order_by("-id")

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return BasketReadSerializer
        return BasketWriteSerializer
