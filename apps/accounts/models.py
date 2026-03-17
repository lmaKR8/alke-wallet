"""
Modelos de la app accounts — Usuario personalizado.

Mapea exactamente la tabla `users` del esquema físico de la Etapa 2.
Extiende AbstractUser para aprovechar el sistema de autenticación de Django.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from apps.wallet.mixins import SoftDeleteManager, SoftDeleteModel


class UserManager(BaseUserManager):
    """
    Manager personalizado para el modelo User con email como campo de autenticación.

    Reemplaza el manager por defecto de AbstractUser para soportar
    creación de usuarios con email en lugar de username.
    """

    def get_queryset(self):
        """Retorna solo usuarios activos (deleted_at IS NULL)."""
        return super().get_queryset().filter(deleted_at__isnull=True)

    def create_user(self, email, user_name, password=None, **extra_fields):
        """
        Crea y guarda un usuario con email, user_name y contraseña.

        Args:
            email (str): Dirección de correo electrónico (campo de autenticación).
            user_name (str): Nombre de usuario visible.
            password (str): Contraseña en texto plano (se hashea internamente).
            **extra_fields: Campos adicionales del modelo.

        Returns:
            User: Instancia del usuario creado.

        Raises:
            ValueError: Si el email está vacío.
        """
        if not email:
            raise ValueError('El correo electrónico es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password=None, **extra_fields):
        """
        Crea y guarda un superusuario con todos los permisos.

        Args:
            email (str): Correo del superusuario.
            user_name (str): Nombre de usuario.
            password (str): Contraseña.
            **extra_fields: Campos adicionales.

        Returns:
            User: Instancia del superusuario creado.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, user_name, password, **extra_fields)


class User(AbstractUser, SoftDeleteModel):
    """
    Modelo de usuario personalizado para Alke Wallet.

    Mapea la tabla `users` del esquema físico de Etapa 2:
        id_user   → id (PK auto, heredado de AbstractUser)
        user_name → user_name (CharField 60)
        email     → email (EmailField 100, UNIQUE, campo de autenticación)
        password  → password (heredado de AbstractUser, con hash)
        created_at, updated_at, deleted_at → heredados de SoftDeleteModel

    El campo USERNAME_FIELD es 'email' en lugar del 'username' por defecto
    de Django, alineándose con el esquema de Etapa 2.
    """

    # Anulamos username de AbstractUser para no requerirlo
    username = None

    user_name = models.CharField(
        max_length=60,
        verbose_name='Nombre de usuario',
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name='Correo electrónico',
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    objects = UserManager()
    all_objects = models.Manager()

    class Meta:
        """Metadatos del modelo User."""

        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['user_name']

    def __str__(self):
        """Representación legible del usuario."""
        return f"{self.user_name} ({self.email})"

    def get_active_accounts(self):
        """
        Retorna todas las cuentas activas del usuario.

        Returns:
            QuerySet: Cuentas activas del usuario.
        """
        return self.accounts.all()
