"""
Modelos de la app transactions — Transaction.

Mapea exactamente la tabla `transactions` del esquema físico de la Etapa 2.
"""

from django.db import models

from apps.wallet.mixins import SoftDeleteModel


class Transaction(SoftDeleteModel):
    """
    Modelo de transacción entre cuentas.

    Mapea la tabla `transactions` del esquema físico de Etapa 2:
        id_transaction      → id (PK auto)
        sender_account_id   → sender_account (FK → Account, NULL=True para depósitos)
        receiver_account_id → receiver_account (FK → Account)
        amount              → amount (NUMERIC 12,2)
        transaction_date    → transaction_date (auto_now_add)
        updated_at, deleted_at → heredados de SoftDeleteModel

    Depósitos externos:
        sender_account = None (no hay cuenta de origen).
        Esto permite representar depósitos y transferencias con el mismo modelo.

    Transferencias:
        sender_account = cuenta origen del remitente.
        receiver_account = cuenta destino del receptor.
    """

    sender_account = models.ForeignKey(
        'wallet.Account',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_transactions',
        verbose_name='Cuenta remitente',
        help_text='NULL indica que es un depósito externo.',
    )
    receiver_account = models.ForeignKey(
        'wallet.Account',
        on_delete=models.CASCADE,
        related_name='received_transactions',
        verbose_name='Cuenta receptora',
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Monto',
    )
    transaction_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de transacción',
    )

    class Meta(SoftDeleteModel.Meta):
        """Metadatos del modelo Transaction."""

        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['-transaction_date']

    def __str__(self):
        """Representación legible de la transacción."""
        if self.sender_account is None:
            return f"Depósito → {self.receiver_account} | {self.amount}"
        return f"{self.sender_account.user.user_name} → {self.receiver_account.user.user_name} | {self.amount}"

    @property
    def transaction_type(self):
        """
        Determina el tipo de transacción.

        Returns:
            str: 'deposito' si no hay cuenta remitente, 'transferencia' en caso contrario.
        """
        if self.sender_account is None:
            return 'deposito'
        return 'transferencia'
