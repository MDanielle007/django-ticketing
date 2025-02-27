from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from functools import wraps
from .models import Ticket

# Decorator to allow only admins
def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            raise PermissionDenied("You do not have permission to perform this action.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Decorator to allow only support staff to update ticket status
def support_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.groups.filter(name='support').exists():
            raise PermissionDenied("Only support staff can update ticket status.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Decorator to allow only the ticket owner to access or modify their tickets
def owner_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        ticket = get_object_or_404(Ticket, pk=kwargs['pk'])
        if request.user != ticket.created_by:
            raise PermissionDenied("You can only access your own tickets.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
