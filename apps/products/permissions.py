from rest_framework import permissions


class IsSellerCompanyOrReadOnly(permissions.BasePermission):
    """Создание товаров доступно только компании-поставщику.

    Просмотр товаров доступен всем пользователям.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if not request.user.is_company:
            return False
        return request.user.company.role == "supplier"


class IsOwnerOfProductOrReadOnly(permissions.BasePermission):
    """Редактирование/удаление товара доступно только владельцу."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user
