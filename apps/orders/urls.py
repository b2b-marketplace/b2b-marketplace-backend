from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.orders.views import OrderViewSet

router = SimpleRouter()
router.register("orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
]
