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
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   └── validators.py
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