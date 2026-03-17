"""
Middleware de autenticación global para Alke Wallet.

Protege todas las rutas privadas sin necesidad de decoradores individuales.
"""

from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    """
    Middleware que intercepta cada request y verifica autenticación.

    Redirige a login si el usuario no está autenticado y la ruta no es pública.
    Agrega el parámetro ?next= para retornar a la página original tras el login.
    """

    def __init__(self, get_response):
        """Inicializa el middleware recibiendo la función de respuesta de Django."""
        self.get_response = get_response

    def __call__(self, request):
        """
        Evalúa cada request entrante.

        Args:
            request: El objeto HttpRequest de Django.

        Returns:
            Redirección a login si no autenticado en ruta privada,
            de lo contrario continúa el flujo normal.
        """
        login_url = reverse('login')
        register_url = reverse('register')

        public_paths = [
            login_url,
            register_url,
            '/admin/',
            '/static/',
            '/media/',
        ]

        # La landing page (/) también es pública
        is_index = request.path == '/'
        is_public_path = is_index or any(
            request.path.startswith(path) for path in public_paths
        )

        if not request.user.is_authenticated and not is_public_path:
            return redirect(f"{login_url}?next={request.path}")

        return self.get_response(request)
