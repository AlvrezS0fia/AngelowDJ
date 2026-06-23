# clientes/models.py
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from website.validators import validar_telefono_colombia, validar_email

class Cliente(models.Model):
    """Modelo Cliente para CRM - Hereda conceptos del Record original"""
    TIPO_DOCUMENTO = (
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('NIT', 'NIT'),
        ('PAS', 'Pasaporte'),
    )
    
    # Campos obligatorios con validaciones robustas
    tipo_documento = models.CharField(max_length=3, choices=TIPO_DOCUMENTO, default='CC')
    numero_documento = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message='El número de documento solo debe contener dígitos'
            )
        ]
    )
    nombre = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                message='El nombre solo debe contener letras y espacios'
            )
        ]
    )
    apellido = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
                message='El apellido solo debe contener letras y espacios'
            )
        ]
    )
    email = models.EmailField(
        max_length=100,
        validators=[validar_email]
    )
    telefono = models.CharField(
        max_length=15,
        validators=[validar_telefono_colombia]
    )
    direccion = models.TextField()
    ciudad = models.CharField(max_length=50)
    departamento = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=10)
    
    # Campos adicionales para el CRM
    fecha_nacimiento = models.DateField(null=True, blank=True)
    notas = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    usuario_registro = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    class Meta:
        ordering = ['-fecha_registro']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'