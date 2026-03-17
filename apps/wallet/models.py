"""
Modelos de la app wallet — Currency y Account.

Mapea exactamente las tablas `currencies` y `accounts` del esquema
físico de la Etapa 2.
"""

from django.conf import settings
from django.db import models

from apps.wallet.mixins import SoftDeleteModel


class Currency(SoftDeleteModel):
    """
    Modelo de moneda disponible en el sistema.

    Mapea la tabla `currencies` del esquema físico de Etapa 2:
        id_currency     → id (PK auto)
        currency_name   → currency_name (VARCHAR 50, UNIQUE)
        currency_symbol → currency_symbol (CHAR 3, UNIQUE)
        created_at, updated_at, deleted_at → heredados de SoftDeleteModel

    Monedas iniciales (seed data): CLP, USD, EUR, CNY, CAD
    """

    currency_name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Nombre de la moneda',
    )
    currency_symbol = models.CharField(
        max_length=3,
        unique=True,
        verbose_name='Símbolo (ISO 4217)',
        help_text='Ejemplo: CLP, USD, EUR',
    )

    class Meta:
        """Metadatos del modelo Currency."""

        verbose_name = 'Moneda'
        verbose_name_plural = 'Monedas'
        ordering = ['currency_name']

    def __str__(self):
        """Representación legible de la moneda."""
        return f"{self.currency_name} ({self.currency_symbol})"


class Account(SoftDeleteModel):
    """
    Modelo de cuenta bancaria/billetera de un usuario.

    Mapea la tabla `accounts` del esquema físico de Etapa 2:
        id_account  → id (PK auto)
        user_id     → user (FK → User)
        currency_id → currency (FK → Currency)
        balance     → balance (NUMERIC 12,2)
        created_at, updated_at, deleted_at → heredados de SoftDeleteModel

    Un usuario puede tener múltiples cuentas en distintas monedas.
    El balance usa DecimalField para precisión monetaria exacta.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts',
        verbose_name='Usuario',
    )
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        related_name='accounts',
        verbose_name='Moneda',
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name='Saldo',
    )

    class Meta:
        """Metadatos del modelo Account."""

        verbose_name = 'Cuenta'
        verbose_name_plural = 'Cuentas'
        ordering = ['-balance']

    def __str__(self):
        """Representación legible de la cuenta."""
        return f"{self.user.user_name} — {self.currency.currency_symbol} {self.balance:,.2f}"

    def deposit(self, amount):
        """
        Incrementa el saldo de la cuenta por el monto indicado.

        Args:
            amount (Decimal): Monto a depositar (debe ser positivo).

        Raises:
            ValueError: Si el monto no es positivo.
        """
        if amount <= 0:
            raise ValueError('El monto del depósito debe ser positivo.')
        self.balance += amount
        self.save()

    def withdraw(self, amount):
        """
        Decrementa el saldo de la cuenta por el monto indicado.

        Args:
            amount (Decimal): Monto a retirar (debe ser positivo y <= balance).

        Raises:
            ValueError: Si el monto supera el saldo disponible.
        """
        if amount <= 0:
            raise ValueError('El monto del retiro debe ser positivo.')
        if amount > self.balance:
            raise ValueError('Saldo insuficiente.')
        self.balance -= amount
        self.save()
