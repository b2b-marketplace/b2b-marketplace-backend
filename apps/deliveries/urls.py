from django.urls import include, path
from rest_framework import routers

from apps.deliveries.views import DeliveryMethodViewSet

router = routers.SimpleRouter()
router.register("delivery-methods", DeliveryMethodViewSet, basename="delivery_methods")

urlpatterns = [path("", include(router.urls))]
