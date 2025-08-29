from rest_framework import permissions


class IsModer(permissions.BasePermission):
    message = "Adding customers not allowed."

    def has_permission(self, request, view):
        return (
                request.user.is_authenticated and
                request.user.groups.filter(name='moders').exists()
        )


class IsOwnerOrModeratorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        if request.user.groups.filter(name='moders').exists():
            if request.method in ['GET', 'HEAD', 'OPTIONS', 'PUT', 'PATCH']:
                return True
            return False
        return obj.owner == request.user


class CanDeleteCourseOrLesson(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            if request.user.groups.filter(name='Модераторы').exists():
                return False
            return obj.owner == request.user or request.user.is_staff
        return True

class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj == request.user