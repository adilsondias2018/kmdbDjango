from rest_framework.permissions import BasePermission


class NeverPermit(BasePermission):
    def has_permission(self, request, views):
        return False

class OnlyAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        print(user)

        return user.is_superuser and user.is_staff

class OnlyCritico(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        print(user)

        return user.is_staff 
