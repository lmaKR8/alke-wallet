"""AppConfig para la aplicación contacts."""

from django.apps import AppConfig


class ContactsConfig(AppConfig):
    """Configuración de la app contacts (búsqueda de usuarios y envío de dinero)."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contacts'
    verbose_name = 'Contactos'
