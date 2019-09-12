from datetime import date

from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    message = "This isn't your event.....3an il legafa."

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        else:
            return False