"""AppConfig para la aplicación wallet."""

from django.apps import AppConfig


class WalletConfig(AppConfig):
    """Configuración de la app wallet (billetera, dashboard, depósitos)."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.wallet'
    verbose_name = 'Billetera'
