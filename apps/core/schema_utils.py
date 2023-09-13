import functools

from django.db.models import QuerySet


def schema_django_filter_warning(model=None):
    """
    Декоратор для исправления ошибки генерации схемы api django-filter для анонимного пользователя.

    Если во вьюсете не указан queryset, надо передать модель.
    See: https://github.com/carltongibson/django-filter/issues/966
    """

    def django_filter_warning(get_queryset_func):
        @functools.wraps(get_queryset_func)
        def get_queryset(self):
            if getattr(self, "swagger_fake_view", False):
                if model:
                    return model.objects.none()
                return QuerySet()
            return get_queryset_func(self)

        return get_queryset

    return django_filter_warning
