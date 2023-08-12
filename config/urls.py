from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from config.settings import DEBUG

api_schema_url_patterns = [
    path(
        route="",
        view=SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        route="redoc/",
        view=SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path(
        route="swagger-ui/",
        view=SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

urlpatterns = [
    path(route="api/v1/schema/", view=include(api_schema_url_patterns)),
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.products.urls")),
]

if DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
