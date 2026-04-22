from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """Allow write access only to the user who owns the profile; read is unrestricted."""

    def has_object_permission(self, request, view, obj):
        """Grant safe methods to everyone; restrict mutations to the profile owner.

        obj is a CustomUser instance, so identity is checked directly against request.user.
        """
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user
