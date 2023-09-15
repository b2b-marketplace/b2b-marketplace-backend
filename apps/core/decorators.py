import functools


def django_filter_anonymoususer_warning_schema(model):
    """Документация swagger.

    Исправляет ошибку swagger, при генерации схемы api с фильтром django-filter для
    аутентифицированного пользователя, когда анонимный пользователь не может получить queryset.

    https://github.com/carltongibson/django-filter/issues/966
    """

    def django_filter_warning(get_queryset_func):
        @functools.wraps(get_queryset_func)
        def get_queryset(self):
            if getattr(self, "swagger_fake_view", False):
                return model.objects.none()
            return get_queryset_func(self)

        return get_queryset

    return django_filter_warning
