from rest_framework import permissions


class IsBuyer(permissions.BasePermission):
    """Корзина доступна только компании-заказчику или физическому лицу."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.personal or request.user.company.role == "customer"
