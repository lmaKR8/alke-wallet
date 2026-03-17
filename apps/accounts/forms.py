"""
Formularios de autenticación para Alke Wallet.

Implementa los formularios de registro e inicio de sesión
siguiendo los patrones de fuente-verdad/django_docs/implementacion_login_django.md
"""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    """
    Formulario de registro de nuevo usuario.

    Extiende UserCreationForm para incluir los campos específicos
    del modelo User personalizado (email y user_name).
    """

    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@correo.com',
        }),
    )
    user_name = forms.CharField(
        max_length=60,
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu nombre',
        }),
    )

    class Meta:
        """Meta configuración del formulario de registro."""

        model = User
        fields = ('user_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        """Aplica clases Bootstrap a los campos de contraseña."""
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'


class LoginForm(AuthenticationForm):
    """
    Formulario de inicio de sesión con email como campo principal.

    Aplica estilos Bootstrap a los campos del formulario de login
    nativo de Django.
    """

    username = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'tu@correo.com',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '••••••••',
        }),
    )
