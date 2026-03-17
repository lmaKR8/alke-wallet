"""Registro de modelos de accounts en el panel de administración."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Configuración del panel admin para el modelo User personalizado.

    Extiende el UserAdmin de Django para adaptarse al modelo con email
    como campo de autenticación principal.
    """

    list_display = ('email', 'user_name', 'is_staff', 'is_active', 'deleted_at')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'user_name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('user_name',)}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Auditoría', {'fields': ('created_at', 'updated_at', 'deleted_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
