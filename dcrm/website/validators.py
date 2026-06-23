# website/validators.py
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

# Expresiones regulares para validaciones
REGEX_EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
REGEX_TELEFONO_COL = r'^3\d{9}$'
REGEX_NOMBRE = r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$'
REGEX_USUARIO = r'^[a-zA-Z0-9_]{3,20}$'
REGEX_CONTRASENA = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'

def validar_email(value):
    """Valida formato de email usando regex"""
    if not re.match(REGEX_EMAIL, value):
        raise ValidationError('El email no tiene un formato válido')
    return value

def validar_telefono_colombia(value):
    """Valida teléfono colombiano (10 dígitos, empieza con 3)"""
    if not re.match(REGEX_TELEFONO_COL, value):
        raise ValidationError('El teléfono debe tener 10 dígitos y empezar con 3 (ej: 3123456789)')
    return value

def validar_nombre_completo(value):
    """Valida nombre completo (solo letras y espacios)"""
    if not re.match(REGEX_NOMBRE, value):
        raise ValidationError('El nombre solo puede contener letras y espacios')
    return value

def validar_usuario(value):
    """Valida nombre de usuario (3-20 caracteres, alfanumérico y guión bajo)"""
    if not re.match(REGEX_USUARIO, value):
        raise ValidationError('El usuario debe tener entre 3 y 20 caracteres alfanuméricos o guión bajo')
    return value

def validar_contrasena(value):
    """Valida contraseña (8+ caracteres, mayúscula, minúscula, número, especial)"""
    if not re.match(REGEX_CONTRASENA, value):
        raise ValidationError('La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial')
    return value

def validar_nombre_producto(value):
    """Valida nombre de producto (sin caracteres especiales peligrosos)"""
    if re.search(r'[<>"\'/]', value):
        raise ValidationError('El nombre del producto no puede contener caracteres especiales peligrosos')
    return value

# Validadores predefinidos para usar en modelos
validar_usuario_regex = RegexValidator(
    regex=REGEX_USUARIO,
    message='El usuario debe tener entre 3 y 20 caracteres alfanuméricos o guión bajo'
)

validar_contrasena_regex = RegexValidator(
    regex=REGEX_CONTRASENA,
    message='La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial'
)