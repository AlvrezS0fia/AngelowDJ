# website/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from .models import UserProfile

def rol_requerido(*roles):
    """
    Decorador para verificar roles de usuario
    CAPA 1: Control de acceso basado en roles
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para acceder a esta página')
                return redirect('website:login')
            
            try:
                profile = request.user.profile
                if profile.rol not in roles:
                    messages.error(request, 'No tienes permiso para acceder a esta página')
                    return HttpResponseForbidden('Acceso denegado')
            except UserProfile.DoesNotExist:
                messages.error(request, 'Perfil de usuario no encontrado')
                return redirect('website:login')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def login_requerido(view_func):
    """
    Decorador para verificar autenticación
    CAPA 2: Autenticación requerida
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para acceder a esta página')
            return redirect('website:login')
        return view_func(request, *args, **kwargs)
    return wrapper

def verificar_bloqueo(view_func):
    """
    Decorador para verificar si el usuario está bloqueado
    CAPA 3: Bloqueo por intentos fallidos
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                profile = request.user.profile
                if profile.bloqueado_hasta and profile.bloqueado_hasta > timezone.now():
                    messages.error(request, 'Tu cuenta está bloqueada temporalmente. Intenta más tarde.')
                    return redirect('website:login')
            except UserProfile.DoesNotExist:
                pass
        return view_func(request, *args, **kwargs)
    return wrapper