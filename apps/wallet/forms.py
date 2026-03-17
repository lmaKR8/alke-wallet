"""
Formulario de depósito para Alke Wallet.
"""

from decimal import Decimal

from django import forms


class DepositForm(forms.Form):
    """
    Formulario para realizar un depósito en una cuenta.

    Valida que el monto sea positivo y tenga formato decimal correcto.
    """

    amount = forms.DecimalField(
        label='Monto a depositar',
        min_value=Decimal('0.01'),
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '0.00',
            'step': '0.01',
            'min': '0.01',
        }),
    )

    def clean_amount(self):
        """
        Valida que el monto sea positivo.

        Returns:
            Decimal: El monto validado.

        Raises:
            ValidationError: Si el monto no es mayor a cero.
        """
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError('El monto debe ser mayor a cero.')
        return amount
