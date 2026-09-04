from rest_framework.permissions import BasePermission
from .models import Item

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
                request.user.is_authenticated and
                request.user.isadmin
        )

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        item_id = view.kwargs.get('id')
        return (
                request.user.is_authenticated and
                Item.objects.filter(
                    id=item_id,
                    user=request.user
                ).exists()
        )

