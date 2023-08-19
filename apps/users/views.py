from django.contrib.auth import get_user_model
from djoser import utils
from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.serializers.companies import (
    MeUserCompanyReadSerializer,
    MeUserCompanyWriteSerializer,
    UserCompanyReadSerializer,
    UserCompanyWriteSerializer,
)

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Кастомный ViewSet для пользователей."""

    def get_serializer_class(self):
        if self.action == "companies" and self.request.method in permissions.SAFE_METHODS:
            return UserCompanyReadSerializer
        elif self.action == "create_company":
            return UserCompanyWriteSerializer

        elif (
            self.action == "me"
            and self.request.method in permissions.SAFE_METHODS
            and self.get_instance().is_company
        ):
            return MeUserCompanyReadSerializer

        elif (
            self.action == "me"
            and self.request.method in ("PUT", "PATCH")
            and self.get_instance().is_company
        ):
            return MeUserCompanyWriteSerializer

        return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == request.user:
            utils.logout_user(self.request)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

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

    @extend_schema(
        request=MeUserCompanyWriteSerializer,
        responses={200: MeUserCompanyReadSerializer},
        methods=["get", "put", "patch"],
    )
    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)
