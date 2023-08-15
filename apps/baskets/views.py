from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.baskets.models import Basket
from apps.baskets.serializers.baskets import BasketReadSerializer, BasketWriteSerializer
from apps.users.models import CustomUser


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all().order_by("-id")
    http_method_names = ["get", "post", "delete"]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return BasketReadSerializer
        return BasketWriteSerializer

    def perform_create(self, serializer):
        # TODO: заглушка, пока не реализована аутентификация
        # После реализации аутентификации, взять юзера из request (self.request.user)
        user = CustomUser.objects.filter(is_company=True).first()
        serializer.save(user=user)

    @action(detail=False, methods=["POST"])
    def create_and_redirect(self, request):
        return Response(
            status=status.HTTP_201_CREATED, headers={"Location": self.reverse_action("mine")}
        )

    @action(detail=False, methods=["get"], url_path="mine")
    def my_basket(self, request):
        return Response({"message": "Моя корзина"})
