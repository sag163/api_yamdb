from rest_framework import permissions


class IsModeratorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'moderator'


class IsAuthorPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.author
