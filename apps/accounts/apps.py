"""AppConfig para la aplicación accounts."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuración de la app accounts (autenticación y usuarios)."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'Cuentas de Usuario'
