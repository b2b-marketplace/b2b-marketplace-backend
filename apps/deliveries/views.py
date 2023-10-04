from rest_framework import viewsets

from apps.deliveries.models import DeliveryMethod
from apps.deliveries.serializers.deliverymethods import DeliveryMethodReadSerializer


class DeliveryMethodViewSet(viewsets.ReadOnlyModelViewSet):
    """Методы доставки."""

    queryset = DeliveryMethod.objects.all()
    serializer_class = DeliveryMethodReadSerializer
