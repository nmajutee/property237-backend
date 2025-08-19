from rest_framework import permissions


class IsAgentOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow agents to create/edit objects.
    """
    def has_permission(self, request, view):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for authenticated agents
        return (request.user and
                request.user.is_authenticated and
                request.user.user_type == 'agent')


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'agent') and hasattr(obj.agent, 'user'):
            return obj.agent.user == request.user

        return False


class IsVerifiedAgent(permissions.BasePermission):
    """
    Permission for verified agents only.
    """
    def has_permission(self, request, view):
        return (request.user and
                request.user.is_authenticated and
                request.user.user_type == 'agent' and
                hasattr(request.user, 'agent_profile') and
                request.user.agent_profile.is_verified)