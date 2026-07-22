from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """Permission to only allow admin users."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsClientOrAdmin(permissions.BasePermission):
    """Permission to allow registered clients and admins."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_client or request.user.is_admin


class IsOwnerOrAdmin(permissions.BasePermission):
    """Permission to only allow owners of an object or admins."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return hasattr(obj, 'user') and obj.user == request.user
