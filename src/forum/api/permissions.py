from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message = "You must be the owner of this object."
    safe_methods = ['PUT']

    def has_permission(self, request, view):
        if request.method in self.safe_methods:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user.author
