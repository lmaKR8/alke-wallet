"""Formularios de la app contacts — alias de contacto y envío de dinero."""

from decimal import Decimal

from django import forms


class ContactAliasForm(forms.Form):
    """Formulario para crear o editar el alias de un contacto."""

    alias = forms.CharField(
        label='Alias (opcional)',
        required=False,
        max_length=60,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Ej: Pelao Loco, Mamá, Trabajo...',
            'autocomplete': 'off',
        }),
    )


class SendMoneyForm(forms.Form):
    """Formulario para enviar dinero a otro usuario."""

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
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError('El monto debe ser mayor a cero.')
        return amount
