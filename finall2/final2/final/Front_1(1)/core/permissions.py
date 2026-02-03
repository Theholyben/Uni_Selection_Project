from rest_framework import permissions

from .models import User


class IsAdminUserRole(permissions.BasePermission):
    """
    فقط کاربرانی که نقش مدیر دارند دسترسی دارند.
    """

    def has_permission(self, request, view) -> bool:
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "role", None) == User.Roles.ADMIN
        )


class IsProfessorUserRole(permissions.BasePermission):
    """
    فقط اساتید.
    """

    def has_permission(self, request, view) -> bool:
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "role", None) == User.Roles.PROFESSOR
        )


class IsStudentUserRole(permissions.BasePermission):
    """
    فقط دانشجویان.
    """

    def has_permission(self, request, view) -> bool:
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and getattr(user, "role", None) == User.Roles.STUDENT
        )


