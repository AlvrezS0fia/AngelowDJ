# website/middleware.py
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponseForbidden
from datetime import timedelta
import re

class SecurityHeadersMiddleware:
    """
    CAPA 4: Headers de seguridad
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Headers de seguridad
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response

class SessionTimeoutMiddleware:
    """
    Middleware para expirar sesión después de inactividad
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            # Verificar si la sesión ha expirado por inactividad
            last_activity = request.session.get('last_activity')
            now = timezone.now()
            
            if last_activity:
                last_activity = timezone.datetime.fromisoformat(last_activity)
                if (now - last_activity).seconds > 3600:  # 1 hora de inactividad
                    # Cerrar sesión automáticamente
                    from django.contrib.auth import logout
                    logout(request)
                    messages.warning(request, 'Tu sesión ha expirado por inactividad')
                    return redirect('website:login')
            
            # Actualizar última actividad
            request.session['last_activity'] = now.isoformat()
        
        response = self.get_response(request)
        return response

class RateLimitMiddleware:
    """
    Middleware para limitar intentos de login
    """
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Verificar si es una solicitud de login
        if request.path == '/accounts/login/' and request.method == 'POST':
            ip = request.META.get('REMOTE_ADDR')
            key = f'login_attempts_{ip}'
            attempts = cache.get(key, 0)
            
            if attempts >= 5:  # Máximo 5 intentos
                messages.error(request, 'Demasiados intentos de login. Espera 5 minutos.')
                return HttpResponseForbidden('Demasiados intentos de login')
            
            # Incrementar contador
            cache.set(key, attempts + 1, timeout=300)  # 5 minutos
        
        response = self.get_response(request)
        return response