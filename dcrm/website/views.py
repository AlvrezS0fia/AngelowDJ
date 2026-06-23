# website/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.cache import cache
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm, UserProfileForm
from .decorators import login_requerido, rol_requerido, verificar_bloqueo
from .models import UserProfile
from .validators import validar_contrasena
import re

def home_view(request):
    """Vista principal - Landing page"""
    if request.user.is_authenticated:
        return redirect('website:dashboard')
    return render(request, 'website/home.html')

def login_view(request):
    """Vista de login con 4 capas de seguridad"""
    if request.user.is_authenticated:
        return redirect('website:dashboard')
    
    form = LoginForm()
    
    if request.method == 'POST':
        # CAPA 1: Rate limiting por IP
        ip = request.META.get('REMOTE_ADDR')
        key = f'login_attempts_{ip}'
        attempts = cache.get(key, 0)
        
        if attempts >= 5:
            messages.error(request, 'Demasiados intentos. Espera 5 minutos.')
            return render(request, 'website/login.html', {'form': form})
        
        # CAPA 2: Sanitización de entrada
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Limpiar caracteres peligrosos
        username = re.sub(r'[<>"\'/]', '', username)
        
        # CAPA 3: Autenticación
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # CAPA 4: Verificar si el usuario está bloqueado
            try:
                profile = user.profile
                if profile.bloqueado_hasta and profile.bloqueado_hasta > timezone.now():
                    messages.error(request, 'Cuenta bloqueada temporalmente. Intenta más tarde.')
                    return render(request, 'website/login.html', {'form': form})
                
                # Resetear intentos fallidos
                profile.intentos_fallidos = 0
                profile.save()
                
            except UserProfile.DoesNotExist:
                pass
            
            login(request, user)
            messages.success(request, f'¡Bienvenido {user.username}!')
            return redirect('website:dashboard')
        else:
            # Incrementar intentos fallidos
            cache.set(key, attempts + 1, timeout=300)
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'website/login.html', {'form': form})

@login_requerido
@verificar_bloqueo
def dashboard_view(request):
    """Dashboard con información del usuario y estadísticas"""
    context = {
        'total_clientes': 0,
        'total_productos': 0,
        'total_pedidos': 0,
    }
    
    # Cargar estadísticas según el rol
    if request.user.profile.is_admin or request.user.profile.is_vendedor:
        from clientes.models import Cliente
        from tienda.models import Producto
        context['total_clientes'] = Cliente.objects.count()
        context['total_productos'] = Producto.objects.filter(activo=True).count()
    
    return render(request, 'website/dashboard.html', context)

def register_view(request):
    """Vista de registro con validaciones"""
    if request.user.is_authenticated:
        return redirect('website:dashboard')
    
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Autenticar automáticamente después del registro
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a ANGELOW')
            return redirect('website:dashboard')
        else:
            messages.error(request, 'Por favor corrige los errores del formulario')
    
    return render(request, 'website/register.html', {'form': form})

@login_required
def logout_view(request):
    """Cerrar sesión"""
    logout(request)
    messages.info(request, 'Sesión cerrada exitosamente')
    return redirect('website:home')

@login_requerido
@verificar_bloqueo
def perfil_view(request):
    """Vista y edición de perfil"""
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado exitosamente')
            return redirect('website:perfil')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'website/profile.html', {
        'form': form,
        'profile': profile
    })

@login_requerido
@rol_requerido('admin')
def admin_view(request):
    """Vista de administración (solo admin)"""
    return render(request, 'website/admin_panel.html')