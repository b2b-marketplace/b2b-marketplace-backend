from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users.serializers import CompanyCreateSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    @action(("get",), detail=False, permission_classes=(AllowAny,))
    def companies(self, request):
        user = User.objects.get_companies()
        page = self.paginate_queryset(user)
        if page is not None:
            serializer = CompanyCreateSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CompanyCreateSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @companies.mapping.post
    def create_company(self, request):
        serializer = CompanyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
