# tienda/context_processors.py
from .models import Carrito, Categoria

def carrito(request):
    """Context processor para el carrito disponible en toda la aplicación"""
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(
            usuario=request.user,
            completado=False
        )
        return {
            'carrito': carrito,
            'carrito_total_items': carrito.total_items,
            'carrito_total_precio': carrito.total_precio
        }
    return {
        'carrito': None,
        'carrito_total_items': 0,
        'carrito_total_precio': 0
    }

def categorias(request):
    """Context processor para categorías disponibles en toda la aplicación"""
    return {
        'categorias_menu': Categoria.objects.filter(activo=True)
    }