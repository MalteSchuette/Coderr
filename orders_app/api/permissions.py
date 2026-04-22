from rest_framework.permissions import BasePermission


class IsCustomerUser(BasePermission):
    """Allow access only to users whose profile type is 'customer'."""

    def has_permission(self, request, view):
        """Return True if the authenticated user has a customer profile."""
        return request.user.profile_type == 'customer'


class IsBusinessOwner(BasePermission):
    """Allow write access only to the business user assigned to the order."""

    def has_object_permission(self, request, view, obj):
        """Return True if the requesting user is the business owner of the order."""
        return obj.business_user == request.user


class IsAdminUser(BasePermission):
    """Allow access only to staff (admin) users."""

    def has_permission(self, request, view):
        """Return True if the authenticated user has staff privileges."""
        return request.user.is_staff
