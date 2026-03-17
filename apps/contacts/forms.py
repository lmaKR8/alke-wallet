"""
Formulario de envío de dinero para Alke Wallet.
"""

from decimal import Decimal

from django import forms


class SendMoneyForm(forms.Form):
    """
    Formulario para enviar dinero a otro usuario.

    Valida que el monto sea positivo y permite un mensaje opcional
    como descripción de la transferencia.
    """

    amount = forms.DecimalField(
        label='Monto a enviar',
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
    message = forms.CharField(
        label='Mensaje (opcional)',
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '¿Para qué es la transferencia?',
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
