"""Modelo Contact para la app contacts — contactos personales del usuario."""

from django.conf import settings
from django.db import models


class Contact(models.Model):
    """
    Contacto personal del usuario autenticado.

    Permite guardar otros usuarios del sistema con un alias personalizado
    para enviarles dinero rápidamente.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contacts',
        verbose_name='Propietario',
    )
    contact_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='saved_as_contact',
        verbose_name='Usuario contacto',
    )
    alias = models.CharField(
        max_length=60,
        blank=True,
        verbose_name='Alias',
        help_text='Apodo o nombre personalizado para este contacto.',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'contact_user')
        ordering = ['-created_at']
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'

    def __str__(self):
        return f"{self.owner.user_name} → {self.contact_user.user_name}"

    @property
    def display_name(self):
        """Alias personalizado o nombre del usuario si no hay alias."""
        return self.alias if self.alias else self.contact_user.user_name
