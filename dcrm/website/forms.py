# website/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .validators import (
    validar_usuario, validar_contrasena,
    validar_email, validar_telefono_colombia
)
from .models import UserProfile
import re

class LoginForm(AuthenticationForm):
    """
    Formulario de login con validaciones
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario',
            'autofocus': True
        }),
        validators=[validar_usuario]
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Limpiar caracteres peligrosos
        username = re.sub(r'[<>"\'/]', '', username)
        return username

class RegisterForm(UserCreationForm):
    """
    Formulario de registro con validaciones robustas
    APLICACIÓN DEL PRINCIPIO DRY: Reutiliza validadores
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico'
        }),
        validators=[validar_email]
    )
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Apellido'
        })
    )
    telefono = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Teléfono (ej: 3123456789)'
        }),
        validators=[validar_telefono_colombia],
        required=False
    )
    rol = forms.ChoiceField(
        choices=UserProfile.ROLES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        required=False
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de usuario (3-20 caracteres)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña (8+ caracteres)'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Limpiar caracteres especiales peligrosos
        username = re.sub(r'[<>"\'/]', '', username)
        # Validar con regex
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            raise ValidationError('El usuario debe tener entre 3 y 20 caracteres alfanuméricos o guión bajo')
        return username
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Crear/actualizar perfil
            profile = user.profile
            profile.telefono = self.cleaned_data.get('telefono', '')
            profile.rol = self.cleaned_data.get('rol', 'cliente')
            profile.save()
        
        return user

class UserProfileForm(forms.ModelForm):
    """Formulario para editar perfil de usuario"""
    class Meta:
        model = UserProfile
        fields = ['telefono', 'direccion', 'avatar', 'rol']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }