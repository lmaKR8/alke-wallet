"""
Mixin de Soft Delete reutilizable para todos los modelos de negocio.

Proporciona:
- Campos de auditoría: created_at, updated_at, deleted_at
- Manager por defecto que excluye registros eliminados (deleted_at IS NULL)
- Manager alternativo all_objects para consultas históricas
- Métodos soft_delete() y restore()
"""

from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    """
    Manager personalizado que filtra registros con deleted_at IS NULL.

    Es el manager por defecto en todos los modelos que hereden SoftDeleteModel.
    Para obtener todos los registros (incluyendo eliminados), usar all_objects.
    """

    def get_queryset(self):
        """Retorna únicamente registros activos (no eliminados)."""
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    """
    Modelo abstracto base con lógica de Soft Delete.

    Todos los modelos de negocio de Alke Wallet heredan de este mixin.
    Implementa el patrón definido en el esquema físico de la Etapa 2,
    donde cada tabla tiene una columna deleted_at TIMESTAMP NULL.

    Campos:
        created_at  (DateTimeField): Timestamp de creación (automático).
        updated_at  (DateTimeField): Timestamp de última modificación (automático).
        deleted_at  (DateTimeField): Timestamp de eliminación lógica (null = activo).

    Managers:
        objects     (SoftDeleteManager): Solo registros activos (por defecto).
        all_objects (Manager): Todos los registros, incluidos los eliminados.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Creado el',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Actualizado el',
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Eliminado el',
        help_text='NULL indica que el registro está activo.',
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        """Declara el modelo como abstracto para uso como mixin."""

        abstract = True

    def soft_delete(self):
        """
        Marca el registro como eliminado settando deleted_at a la hora actual.

        No elimina físicamente el registro de la base de datos.
        """
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """
        Restaura un registro eliminado settando deleted_at a None.

        El registro vuelve a aparecer en las consultas normales (objects).
        """
        self.deleted_at = None
        self.save()

    @property
    def is_deleted(self):
        """Retorna True si el registro ha sido eliminado lógicamente."""
        return self.deleted_at is not None
