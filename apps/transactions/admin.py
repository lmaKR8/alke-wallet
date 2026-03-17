"""Registro de modelos de transactions en el panel de administración."""

from django.contrib import admin

from apps.transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Configuración del panel admin para el modelo Transaction."""

    list_display = (
        'id', 'transaction_type', 'sender_account', 'receiver_account',
        'amount', 'transaction_date', 'deleted_at',
    )
    list_filter = ('transaction_date',)
    search_fields = (
        'sender_account__user__user_name',
        'receiver_account__user__user_name',
    )
    readonly_fields = ('transaction_date', 'created_at', 'updated_at')
    raw_id_fields = ('sender_account', 'receiver_account')
