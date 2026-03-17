"""Registro de modelos de wallet en el panel de administración."""

from django.contrib import admin

from apps.wallet.models import Account, Currency


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    """Configuración del panel admin para el modelo Currency."""

    list_display = ('currency_name', 'currency_symbol', 'created_at', 'deleted_at')
    search_fields = ('currency_name', 'currency_symbol')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """Configuración del panel admin para el modelo Account."""

    list_display = ('user', 'currency', 'balance', 'created_at', 'deleted_at')
    list_filter = ('currency',)
    search_fields = ('user__user_name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user',)
