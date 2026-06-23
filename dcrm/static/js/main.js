// static/js/main.js
document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // SPA - Navegación sin recarga de página
    // ============================================
    const links = document.querySelectorAll('[data-spa="true"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('href');
            if (url && url !== '#') {
                cargarContenido(url);
            }
        });
    });
    
    // ============================================
    // Alerta con fade out automático
    // ============================================
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade');
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 4000);
    });
    
    // ============================================
    // Favoritos - Toggle con AJAX
    // ============================================
    document.querySelectorAll('.favorite-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const url = this.dataset.url;
            const icon = this.querySelector('i');
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'added') {
                    this.classList.add('active');
                    icon.classList.remove('far');
                    icon.classList.add('fas');
                } else {
                    this.classList.remove('active');
                    icon.classList.remove('fas');
                    icon.classList.add('far');
                }
                mostrarNotificacion(data.message, 'success');
            })
            .catch(error => {
                mostrarNotificacion('Error al actualizar favorito', 'danger');
            });
        });
    });
    
    // ============================================
    // Carrito - Agregar con AJAX
    // ============================================
    document.querySelectorAll('.add-to-cart').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.dataset.url;
            const productId = this.dataset.productId;
            const talla = document.querySelector(`#talla-${productId}`)?.value || 'M';
            const cantidad = document.querySelector(`#cantidad-${productId}`)?.value || 1;
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    talla: talla,
                    cantidad: cantidad
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    actualizarCarrito(data.total_items);
                    mostrarNotificacion(data.message, 'success');
                } else {
                    mostrarNotificacion(data.message, 'warning');
                }
            })
            .catch(error => {
                mostrarNotificacion('Error al agregar al carrito', 'danger');
            });
        });
    });
    
    // ============================================
    // Función para obtener token CSRF
    // ============================================
    function getCsrfToken() {
        const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
        return cookie ? cookie.split('=')[1] : '';
    }
    
    // ============================================
    // Función para cargar contenido (SPA)
    // ============================================
    function cargarContenido(url) {
        const mainContent = document.getElementById('mainContent');
        if (!mainContent) return;
        
        // Mostrar loader
        mainContent.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-3 text-muted">Cargando contenido...</p>
            </div>
        `;
        
        fetch(url, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newContent = doc.getElementById('mainContent');
            
            if (newContent) {
                mainContent.innerHTML = newContent.innerHTML;
                // Actualizar URL sin recargar
                history.pushState(null, '', url);
            }
        })
        .catch(error => {
            mainContent.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle"></i>
                    Error al cargar el contenido. Por favor, recarga la página.
                </div>
            `;
        });
    }
    
    // ============================================
    // Función para actualizar el badge del carrito
    // ============================================
    function actualizarCarrito(total) {
        const badge = document.querySelector('.carrito-badge');
        if (badge) {
            badge.textContent = total;
            if (total > 0) {
                badge.classList.remove('invisible');
            } else {
                badge.classList.add('invisible');
            }
        }
    }
    
    // ============================================
    // Función para mostrar notificaciones
    // ============================================
    function mostrarNotificacion(mensaje, tipo = 'success') {
        const container = document.querySelector('.container.mt-4') || document.body;
        const alert = document.createElement('div');
        alert.className = `alert alert-${tipo} alert-dismissible fade show animate__animated animate__fadeInDown`;
        alert.innerHTML = `
            <i class="fas fa-${tipo === 'success' ? 'check-circle' : tipo === 'danger' ? 'exclamation-circle' : 'info-circle'}"></i>
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        container.prepend(alert);
        
        setTimeout(() => {
            alert.classList.add('fade');
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    }
    
    // ============================================
    // Validación de formularios en tiempo real
    // ============================================
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = this.querySelectorAll('.form-control');
            let isValid = true;
            
            inputs.forEach(input => {
                if (input.hasAttribute('required') && !input.value.trim()) {
                    input.classList.add('is-invalid');
                    isValid = false;
                } else {
                    input.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                mostrarNotificacion('Por favor, completa todos los campos requeridos', 'warning');
            }
        });
    });
    
    // ============================================
    // Búsqueda en tiempo real
    // ============================================
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        let timeoutId;
        searchInput.addEventListener('input', function() {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => {
                const query = this.value;
                const url = new URL(window.location.href);
                url.searchParams.set('q', query);
                cargarContenido(url.toString());
            }, 300);
        });
    }
    
    // ============================================
    // Manejo de navegación con botones atrás/adelante
    // ============================================
    window.addEventListener('popstate', function() {
        if (window.location.href !== this.location.href) {
            cargarContenido(window.location.href);
        }
    });
});

// ============================================
// Exportar funciones para uso global
// ============================================
window.mostrarNotificacion = mostrarNotificacion;
window.actualizarCarrito = actualizarCarrito;