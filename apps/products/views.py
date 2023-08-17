from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, parsers, permissions, viewsets

from apps.products import serializers
from apps.products.filters import CategoryFilter, ProductFilter
from apps.products.models import Category, Product
from apps.users.models import CustomUser


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """ Вьюсет для работы с категориями. """

    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CategoryFilter


class ProductViewSet(viewsets.ModelViewSet):
    """ Вьюсет для работы с продуктами. """

    queryset = Product.objects.all().order_by("-id")
    serializer_class = serializers.ProductReadSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_serializer_class(self):
        """ Возвращает класс сериализатора. """

        if self.request.method in permissions.SAFE_METHODS:
            return serializers.ProductReadSerializer
        return serializers.ProductWriteSerializer

    def perform_create(self, serializer):
        # TODO: заглушка, пока не реализована аутентификация
        # После реализации аутентификации, взять юзера из request (self.request.user)
        user = CustomUser.objects.filter(is_company=True).first()
        serializer.save(user=user)
