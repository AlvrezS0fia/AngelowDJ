# tienda/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from website.validators import validar_nombre_producto

class Categoria(models.Model):
    """Categorías de productos"""
    nombre = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=50, blank=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = 'Categorías'

class Producto(models.Model):
    """Modelo Producto con validaciones robustas"""
    TALLAS = (
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    )
    
    nombre = models.CharField(
        max_length=100,
        validators=[validar_nombre_producto]
    )
    slug = models.SlugField(unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.CharField(max_length=50, blank=True)
    precio = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    precio_oferta = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)]
    )
    descripcion = models.TextField()
    tallas_disponibles = models.CharField(max_length=100, help_text="Separadas por coma: XS,S,M,L,XL")
    imagenes = models.JSONField(default=list, help_text="Lista de URLs de imágenes")
    stock = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    reseñas = models.PositiveIntegerField(default=0)
    caracteristicas = models.JSONField(default=dict, help_text="Características del producto")
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre
    
    @property
    def precio_final(self):
        return self.precio_oferta if self.precio_oferta else self.precio
    
    @property
    def tiene_oferta(self):
        return self.precio_oferta is not None and self.precio_oferta < self.precio
    
    @property
    def imagen_principal(self):
        return self.imagenes[0] if self.imagenes else '/static/img/default-product.jpg'
    
    @property
    def tallas_lista(self):
        return [t.strip() for t in self.tallas_disponibles.split(',')]
    
    class Meta:
        ordering = ['-destacado', '-fecha_creacion']

class Carrito(models.Model):
    """Carrito de compras por usuario"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    completado = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Carrito de {self.usuario.username}"
    
    @property
    def total_items(self):
        return sum(item.cantidad for item in self.items.all())
    
    @property
    def total_precio(self):
        return sum(item.subtotal for item in self.items.all())

class CarritoItem(models.Model):
    """Items del carrito"""
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    talla = models.CharField(max_length=3, choices=Producto.TALLAS)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['carrito', 'producto', 'talla']
    
    def __str__(self):
        return f"{self.producto.nombre} - {self.talla} x {self.cantidad}"
    
    @property
    def subtotal(self):
        return self.producto.precio_final * self.cantidad

class Favorito(models.Model):
    """Productos favoritos por usuario"""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['usuario', 'producto']
    
    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre}"