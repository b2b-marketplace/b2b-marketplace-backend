from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (
            request.user.personal
            or request.user.is_company
            and request.user.company.role == "customer"
        )

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsSupplier(permissions.BasePermission):
    """Продавец может просматривать/редактировать заказы только со своими товарами."""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if not request.user.is_company:
            return False
        return request.user.company.role == "supplier"

    def has_object_permission(self, request, view, obj):
        return obj.order_products.filter(user=request.user).exists()
