from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Você precisa fazer login para acessar esta área.')
            return redirect('admin_panel:login')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, 'Você não tem permissão para acessar esta área.')
            return redirect('pages:home')
        return view_func(request, *args, **kwargs)
    return wrapper
