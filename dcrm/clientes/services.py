# clientes/services.py
from django.db.models import Q
from .models import Cliente

class ClienteService:
    """Servicio para la gestión de clientes - Aplicación del principio DRY"""
    
    @staticmethod
    def obtener_clientes_filtrados(query='', estado='todos', departamento=''):
        """Obtener clientes con filtros aplicados"""
        clientes = Cliente.objects.filter(activo=True if estado != 'inactivos' else False)
        
        # Si 'todos' incluir activos e inactivos
        if estado == 'todos':
            clientes = Cliente.objects.all()
        
        # Búsqueda por texto
        if query:
            clientes = clientes.filter(
                Q(nombre__icontains=query) |
                Q(apellido__icontains=query) |
                Q(email__icontains=query) |
                Q(numero_documento__icontains=query) |
                Q(telefono__icontains=query)
            )
        
        # Filtro por departamento
        if departamento:
            clientes = clientes.filter(departamento__icontains=departamento)
        
        return clientes.order_by('-fecha_registro')
    
    @staticmethod
    def obtener_clientes_por_departamento():
        """Obtener clientes agrupados por departamento"""
        from django.db.models import Count
        return Cliente.objects.values('departamento').annotate(
            total=Count('id')
        ).order_by('-total')
    
    @staticmethod
    def obtener_estadisticas():
        """Obtener estadísticas de clientes"""
        from django.db.models import Count, Avg, Q
        from django.utils import timezone
        from datetime import timedelta
        
        total = Cliente.objects.count()
        activos = Cliente.objects.filter(activo=True).count()
        nuevos_30_dias = Cliente.objects.filter(
            fecha_registro__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        return {
            'total': total,
            'activos': activos,
            'inactivos': total - activos,
            'nuevos_30_dias': nuevos_30_dias,
        }