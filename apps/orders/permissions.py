from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.id != int(view.kwargs["user_id"]):
            return False
        return request.user.personal or request.user.company.role == "customer"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
