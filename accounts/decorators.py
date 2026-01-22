from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def require_role(role_name):
    """Decorator to require a specific user role"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            try:
                profile = request.user.profile
                if profile.role and profile.role.role_name == role_name:
                    return view_func(request, *args, **kwargs)
            except:
                pass
            
            messages.error(request, 'Access denied. You do not have permission to access this page.')
            return redirect('dashboard')
        
        return wrapper
    return decorator


def require_permission(permission_name):
    """Decorator to require a specific permission"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            try:
                profile = request.user.profile
                if profile.has_permission(permission_name):
                    return view_func(request, *args, **kwargs)
            except:
                pass
            
            messages.error(request, 'Access denied. You do not have this permission.')
            return redirect('dashboard')
        
        return wrapper
    return decorator


def require_admin(view_func):
    """Decorator to require admin role"""
    return require_role('admin')(view_func)


def require_email_verified(view_func):
    """Decorator to require email verification"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        try:
            profile = request.user.profile
            if not profile.is_email_verified:
                messages.warning(request, 'Please verify your email first.')
                return redirect('profile')
        except:
            pass
        
        return view_func(request, *args, **kwargs)
    
    return wrapper
