from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.orders.views import OrderViewSet, SupplierOrderViewSet

router = SimpleRouter()
router.register("orders", OrderViewSet, basename="orders")
router.register("supplier-orders", SupplierOrderViewSet, basename="supplier_orders")

urlpatterns = [
    path("", include(router.urls)),
]
