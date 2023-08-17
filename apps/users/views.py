from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.serializers.companies import (
    UserCompanyReadSerializer,
    UserCompanyWriteSerializer,
)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Кастомный ViewSet для пользователей."""

    def get_serializer_class(self):
        if self.action == "companies":
            return UserCompanyReadSerializer
        elif self.action == "create_company":
            return UserCompanyWriteSerializer
        else:
            return super().get_serializer_class()

    @extend_schema(responses={200: UserCompanyReadSerializer(many=True)})
    @action(("get",), detail=False, permission_classes=(AllowAny,))
    def companies(self, request):
        """Получение списка компаний."""

        user = User.objects.get_companies()
        page = self.paginate_queryset(user)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(responses={201: UserCompanyWriteSerializer})
    @companies.mapping.post
    def create_company(self, request):
        """Создание компании."""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
