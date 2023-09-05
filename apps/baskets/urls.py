from django.urls import include, path
from rest_framework import routers

from apps.baskets.views import BasketViewSet

router = routers.DefaultRouter()
router.register("baskets", BasketViewSet, basename="baskets")

urlpatterns = [path("", include(router.urls))]
