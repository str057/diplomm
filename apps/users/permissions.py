from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Разрешение только для администраторов."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "admin"
        )


class IsTeacher(permissions.BasePermission):
    """Разрешение для преподавателей и администраторов."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ["teacher", "admin"]


class IsStudent(permissions.BasePermission):
    """Разрешение для студентов."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == "student"
        )


class IsOwnerOrTeacher(permissions.BasePermission):
    """Разрешение владельцу объекта или преподавателю/администратору."""

    def has_object_permission(self, request, view, obj):
        if request.user.role in ["teacher", "admin"]:
            return True
        return hasattr(obj, "user") and obj.user == request.user
