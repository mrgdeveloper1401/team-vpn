from rest_framework import permissions


class NotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsOwnerOrIsAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.id == request.user.id or request.user.is_staff:
            return True


class IsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
