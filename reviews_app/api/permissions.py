from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomerUser(BasePermission):
    """Allow access only to users whose profile type is 'customer'."""

    def has_permission(self, request, view):
        """Return True if the authenticated user has a customer profile."""
        return request.user.profile_type == 'customer'


class IsReviewerOrReadOnly(BasePermission):
    """Allow write access only to the user who authored the review; read is unrestricted."""

    def has_object_permission(self, request, view, obj):
        """Grant safe methods to everyone; restrict mutations to the original reviewer."""
        if request.method in SAFE_METHODS:
            return True
        return obj.reviewer == request.user
