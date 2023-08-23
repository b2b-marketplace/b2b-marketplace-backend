from rest_framework import permissions


class IsBuyer(permissions.BasePermission):
    """Создание корзины доступно только компании-заказчику или физическому лицу."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return not request.user.is_company or request.user.company.role == "customer"
