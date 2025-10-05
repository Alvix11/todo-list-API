from rest_framework import permissions

class IsTaskOwner(permissions.BasePermission):
    """
    Permission that verifies if the user is the creator of the task
    """
    def has_object_permission(self, request, view, obj):
        # Always allow safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.user == request.user