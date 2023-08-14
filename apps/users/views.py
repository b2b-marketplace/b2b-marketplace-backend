from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.serializers.companies import CompanySerializer, UserReadSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    def get_serializer_class(self):
        if self.action == "companies":
            return UserReadSerializer
        elif self.action == "create_company":
            return CompanySerializer
        else:
            return super().get_serializer_class()

    @action(("get",), detail=False, permission_classes=(AllowAny,))
    def companies(self, request):
        user = User.objects.get_companies()
        page = self.paginate_queryset(user)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @companies.mapping.post
    def create_company(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
