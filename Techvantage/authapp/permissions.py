# your_app/permissions.py

from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser  # Import AnonymousUser

class IsFirebaseAuthenticated(BasePermission):
    """
    Custom permission to allow access only to authenticated Firebase users.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and not an instance of AnonymousUser
        return request.user and not isinstance(request.user, AnonymousUser) and request.user.is_authenticated
