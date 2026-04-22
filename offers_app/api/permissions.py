from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBusinessUser(BasePermission):
    """Allow access only to users whose profile type is 'business'."""

    def has_permission(self, request, view):
        """Return True if the authenticated user has a business profile."""
        return request.user.profile_type == 'business'


class IsOwnerOrReadOnly(BasePermission):
    """Allow write access only to the user who owns the offer; read is unrestricted."""

    def has_object_permission(self, request, view, obj):
        """Grant safe methods to everyone; restrict mutations to the offer owner."""
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
