# permissions.py is a Python file that defines custom permission classes for a Django REST Framework application. 
# These classes are used to control access to certain views based on the user's role and authentication status.
from rest_framework.permissions import BasePermission


class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'Admin')


class IsEmployeeUserRole(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role in ['Admin', 'Employee']) 