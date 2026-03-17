"""
Vistas de autenticación para Alke Wallet.

Implementa login, registro y logout siguiendo los patrones de
fuente-verdad/django_docs/implementacion_login_django.md
"""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from apps.accounts.forms import LoginForm, RegisterForm


class CustomLoginView(LoginView):
    """
    Vista de inicio de sesión personalizada.

    Extiende LoginView de Django para usar el formulario con estilos Bootstrap
    y redirigir a usuarios ya autenticados al dashboard.
    """

    template_name = 'accounts/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        """
        Procesa el formulario de login cuando es válido.

        Muestra un mensaje de bienvenida y redirige al dashboard.

        Args:
            form (LoginForm): Formulario de login validado.

        Returns:
            HttpResponse: Redirección al dashboard.
        """
        response = super().form_valid(form)
        messages.success(
            self.request,
            f'¡Bienvenido/a, {self.request.user.user_name}!'
        )
        return response

    def form_invalid(self, form):
        """
        Maneja el formulario de login cuando es inválido.

        Muestra un mensaje de error antes de retornar el formulario.

        Args:
            form (LoginForm): Formulario de login con errores.

        Returns:
            HttpResponse: Renderizado del formulario con errores.
        """
        messages.error(self.request, 'Correo o contraseña incorrectos.')
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    """
    Vista de cierre de sesión.

    Usa el LogoutView de Django con redirección configurada en settings.py
    (LOGOUT_REDIRECT_URL = 'login').
    """

    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        """
        Muestra un mensaje de desconexión antes de redirigir.

        Args:
            request: El objeto HttpRequest de Django.

        Returns:
            HttpResponse: Redirección a la página de login.
        """
        messages.info(request, 'Sesión cerrada correctamente.')
        return super().dispatch(request, *args, **kwargs)


def register_view(request):
    """
    Vista de registro de nuevo usuario (FBV).

    GET: Muestra el formulario de registro vacío.
    POST: Valida el formulario, crea el usuario, hace login automático
          y redirige al dashboard.

    Args:
        request: El objeto HttpRequest de Django.

    Returns:
        HttpResponse: Redirige a dashboard si POST exitoso,
                      renderiza el formulario en caso contrario.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'¡Cuenta creada! Bienvenido/a, {user.user_name}.')
            return redirect('dashboard')
        messages.error(request, 'Por favor corrige los errores del formulario.')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})
