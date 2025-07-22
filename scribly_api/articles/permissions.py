from rest_framework import permissions

class ArticlePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user and request.user.is_authenticated

        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_authenticated
        return False


    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
