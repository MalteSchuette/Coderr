from rest_framework.permissions import BasePermission

class IsCustomerUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.profile_type == 'customer'

class IsBusinessOwner(BasePermission):
    def has_object_permission(self, request, view, obj):

        return obj.business_user == request.user

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):

        return request.user.is_staff