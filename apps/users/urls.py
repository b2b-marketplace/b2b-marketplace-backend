from django.urls import include, path

from apps.core.routers import DynamicRouter
from apps.users.views import CustomUserViewSet

router = DynamicRouter()
router.register("users", CustomUserViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
