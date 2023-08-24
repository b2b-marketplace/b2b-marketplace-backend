from django.urls import include, path
from rest_framework.routers import SimpleRouter

from apps.orders.views import OrderViewSet

router = SimpleRouter()
router.register(r"users/(?P<user_id>\d+)/orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
]
