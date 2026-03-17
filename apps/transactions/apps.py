"""AppConfig para la aplicación transactions."""

from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    """Configuración de la app transactions (historial y movimientos)."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.transactions'
    verbose_name = 'Transacciones'
