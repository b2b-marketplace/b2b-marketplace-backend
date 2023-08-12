from django.urls import include, path
from rest_framework import routers

from apps.products import views

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet)

urlpatterns = [path("", include(router.urls))]
