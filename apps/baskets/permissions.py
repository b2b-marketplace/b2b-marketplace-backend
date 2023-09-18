from rest_framework import permissions


class IsBuyer(permissions.BasePermission):
    """Разрешение для покупателя.

    Используется при создании корзины.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.personal or request.user.company.role == "customer"
