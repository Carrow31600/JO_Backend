from rest_framework.permissions import BasePermission

# accès uniquement au superuser
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser

# accès au staff et au superuser
class IsStaffOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)

# accès à l'utilisateur connecté sur ses propres objets et au superuser
class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated and obj == request.user) or request.user.is_superuser
