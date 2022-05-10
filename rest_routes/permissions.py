from django.contrib.auth.decorators import permission_required, login_required
from django.http import HttpRequest
from rest_framework.permissions import BasePermission


@login_required
def suspend_user(request:HttpRequest):
    """
    If the user has the permission to suspend a user, then suspend the user
    
    :param request: The request object that was sent to the view
    :type request: HttpRequest
    :return: A boolean value
    """
    
    if request.user.has_perm("user.can_suspend_user"):
        # Suspend user logic
        return True
    return False


class SuspendUserPerm(BasePermission):
    
    def has_permission(self, request, view):
        pass
    
    def has_object_permission(self, request, view, obj):
        if obj.has_perm("user.can_suspend_user"):
            
            pass