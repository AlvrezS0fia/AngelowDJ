# dcrm/dcrm/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    path('clientes/', include('clientes.urls')),
    path('tienda/', include('tienda.urls')),
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# website/urls.py
from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/perfil/', views.perfil_view, name='perfil'),
    path('admin-panel/', views.admin_view, name='admin_panel'),
]

# clientes/urls.py
from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.cliente_list_view, name='list'),
    path('nuevo/', views.cliente_create_view, name='create'),
    path('<int:pk>/', views.cliente_detail_view, name='detail'),
    path('editar/<int:pk>/', views.cliente_update_view, name='update'),
    path('eliminar/<int:pk>/', views.cliente_delete_view, name='delete'),
    path('exportar/', views.cliente_export_view, name='export'),
    path('api/', views.cliente_api_view, name='api'),
]

# tienda/urls.py
from django.urls import path
from . import views

app_name = 'tienda'

urlpatterns = [
    path('', views.producto_list_view, name='productos'),
    path('producto/<slug:slug>/', views.producto_detail_view, name='detalle'),
    path('categoria/<slug:slug>/', views.producto_por_categoria_view, name='categoria'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_carrito_view, name='agregar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_carrito_item_view, name='eliminar_carrito'),
    path('carrito/actualizar/', views.actualizar_carrito_view, name='actualizar_carrito'),
    path('favoritos/', views.favoritos_view, name='favoritos'),
    path('favoritos/toggle/<int:producto_id>/', views.toggle_favorito_view, name='toggle_favorito'),
    path('api/productos/', views.api_productos_view, name='api_productos'),
    path('api/carrito/', views.api_carrito_view, name='api_carrito'),
]