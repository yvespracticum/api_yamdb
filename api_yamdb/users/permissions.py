from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_admin


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin or request.user.is_superuser
        )


class IsOwnerAdminModerator(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return any([obj.author == request.user,
                       request.user.is_superuser,
                       request.user.is_admin,
                       request.user.is_moderator])
        return request.method in SAFE_METHODS
