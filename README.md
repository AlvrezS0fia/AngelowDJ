# DCRM - Sistema de Gestión de Tienda Online

## Estructura del Proyecto

```
AngelowDJ/
├── dcrm/                    # Proyecto Django principal
│   ├── dcrm/                # Configuración del proyecto
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── settings.py
│   ├── static/              # Archivos estáticos
│   │   ├── css/
│   │   │   ├── bootstrap.min.css
│   │   │   └── styles.css
│   │   ├── js/
│   │   │   ├── bootstrap.bundle.min.js
│   │   │   └── main.js
│   │   └── img/
│   │       └── logo.svg
│   ├── templates/
│   │   ├── base.html
│   │   └── sidebar.html
│   ├── clientes/            # App de gestión de clientes
│   │   ├── templates/
│   │   │   └── clientes/
│   │   │       ├── cliente_confirm_delete.html
│   │   │       ├── cliente_detail.html
│   │   │       ├── cliente_form.html
│   │   │       └── cliente_list.html
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── services.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── tienda/              # App de tienda online
│   │   ├── templates/
│   │   │   └── tienda/
│   │   │       ├── carrito.html
│   │   │       ├── favoritos.html
│   │   │       ├── producto_detail.html
│   │   │       ├── producto_list.html
│   │   │       └── includes/
│   │   │           ├── carrito_widget.html
│   │   │           └── producto_card.html
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── services.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── website/             # App principal del sitio
│   │   ├── templates/
│   │   │   └── website/
│   │   │       ├── base.html
│   │   │       ├── dashboard.html
│   │   │       ├── home.html
│   │   │       ├── login.html
│   │   │       ├── profile.html
│   │   │       └── register.html
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── decorators.py
│   │   ├── forms.py
│   │   ├── middleware.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── validators.py
│   │   └── views.py
│   └── manage.py
├── docs/
│   ├── README.md
│   ├── requirements.txt
│   └── UML/
│       ├── diagrama_clases.puml
│       ├── diagrama_componentes.puml
│       ├── diagrama_despliegue.puml
│       └── diagrama_secuencia.puml
├── .env
├── .gitignore
├── db.sqlite3
└── test_mysql.py
```

## Requisitos
- Django==4.2.11
- PyMySQL==1.1.3
- python-dotenv==1.0.1
- sqlparse==0.4.4

## Seguridad Implementada

El sistema incluye múltiples capas de seguridad:

### 1. Validaciones Robustas (website/validators.py)
- Validación de email con regex
- Validación de teléfono colombiano (10 dígitos, empieza con 3)
- Validación de nombre completo (solo letras y espacios)
- Validación de usuario (3-20 caracteres alfanuméricos)
- Validación de contraseña (8+ caracteres, mayúscula, minúscula, número y especial)

### 2. Decoradores de Seguridad (website/decorators.py)
- `login_requerido`: Verifica autenticación del usuario
- `rol_requerido`: Control de acceso basado en roles (admin, vendedor, cliente)
- `verificar_bloqueo`: Bloqueo por intentos fallidos

### 3. Login con 4 Capas de Seguridad (website/views.py)
- **Capa 1**: Rate limiting por IP (máximo 5 intentos en 5 minutos)
- **Capa 2**: Sanitización de entrada (elimina caracteres peligrosos `<, >, ", ', /`)
- **Capa 3**: Autenticación segura con Django
- **Capa 4**: Verificación de cuenta bloqueada

### 4. Middlewares de Seguridad (website/middleware.py)
- **SecurityHeadersMiddleware**: Headers HTTP de seguridad (X-Frame-Options, X-XSS-Protection, etc.)
- **SessionTimeoutMiddleware**: Cierra sesión tras 1 hora de inactividad
- **RateLimitMiddleware**: Limita intentos de login a nivel middleware

## Modelos Principales

### UserProfile (website/models.py)
Extensión del modelo User con campos adicionales:
- `rol`: Rol del usuario (admin, vendedor, cliente)
- `telefono`, `direccion`, `avatar`
- `intentos_fallidos` y `bloqueado_hasta`: Gestión de bloqueo por intentos fallidos
- Señales automáticas: Crea/actualiza perfil al crear/editar usuario

### Tienda (tienda/models.py)
- **Categoria**: Organización de productos con nombre, slug y descripción
- **Producto**: Información completa (precio, oferta, descripción, tallas, imágenes, stock)
- **Carrito** y **CarritoItem**: Gestión de carrito de compras
- **Favorito**: Productos favoritos por usuario

### Clientes (clientes/models.py)
- **Cliente**: Información de cliente con tipo de documento, nombre, contacto
- Integración con `User` mediante campo `usuario_registro`

## Propósito del Sistema

DCRM es un sistema de gestión de tienda online que permite:
- Gestión de usuarios con roles y permisos
- Administración de clientes (CRUD completo)
- Catálogo de productos con categorías
- Carrito de compras funcional
- Gestión de productos favoritos
- Seguridad multicapa para proteger la aplicación

## Cambios Recientes

### Implementación de Seguridad Multicapa
- **validators.py**: Agregadas validaciones regex para email, teléfono, usuario y contraseña
- **decorators.py**: Creados decoradores `login_requerido`, `rol_requerido`, `verificar_bloqueo`
- **views.py**: Login con 4 capas de seguridad (rate limiting, sanitización, autenticación, bloqueo)
- **middleware.py**: Implementados 3 middlewares de seguridad (SecurityHeaders, SessionTimeout, RateLimit)
- **models.py (website)**: Modelo UserProfile con gestión de roles y bloqueo por intentos fallidos
- **forms.py**: Integradas validaciones en LoginForm y RegisterForm

## Instalación y Configuración

```bash
# Instalar dependencias
pip install -r requirements.txt

# Migrar base de datos
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

## Para Qué Sirve

Este sistema permite gestionar una tienda online completa con:
- **Autenticación segura**: Registro y login con validaciones en 4 capas
- **Gestión de roles**: Administradores, vendedores y clientes con permisos distintos
- **Catálogo de productos**: Con categorías, ofertas y gestión de stock
- **Carrito de compras**: Agregar, modificar y eliminar productos
- **Favoritos**: Marcar productos preferidos
- **CRM integrado**: Gestión de clientes con historial y notas