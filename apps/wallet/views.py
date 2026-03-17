"""
Vistas de la app wallet — landing, dashboard y depósitos.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.transactions.models import Transaction
from apps.wallet.forms import DepositForm
from apps.wallet.models import Account, Currency


def index_view(request):
    """
    Vista pública de la landing page.

    Redirige al dashboard si el usuario ya está autenticado.
    Es una ruta pública (no requiere login).

    Args:
        request: El objeto HttpRequest de Django.

    Returns:
        HttpResponse: Landing page o redirección al dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing/index.html')


@login_required
def dashboard_view(request):
    """
    Vista del panel principal (dashboard) del usuario autenticado.

    Obtiene todas las cuentas activas del usuario, calcula el saldo
    en la moneda principal (CLP) y prepara el contexto para el template.

    Args:
        request: El objeto HttpRequest de Django.

    Returns:
        HttpResponse: Template del dashboard con contexto de cuentas.
    """
    accounts = Account.objects.filter(
        user=request.user
    ).select_related('currency').order_by('currency__currency_symbol')

    # Buscar cuenta principal CLP del usuario (o la primera disponible)
    primary_account = accounts.filter(currency__currency_symbol='CLP').first()
    if primary_account is None:
        primary_account = accounts.first()

    context = {
        'accounts': accounts,
        'primary_account': primary_account,
    }
    return render(request, 'wallet/dashboard.html', context)


@login_required
def deposit_view(request):
    """
    Vista para realizar un depósito en la cuenta del usuario.

    GET: Muestra el formulario de depósito con el saldo actual.
    POST: Valida el formulario, crea una Transaction con sender_account=None
          (indicando que es un depósito externo) y actualiza el balance.

    Args:
        request: El objeto HttpRequest de Django.

    Returns:
        HttpResponse: Formulario de depósito o redirección al dashboard.
    """
    # Obtener cuenta principal CLP del usuario
    account = Account.objects.filter(
        user=request.user,
        currency__currency_symbol='CLP',
    ).first()

    if account is None:
        # Si no tiene cuenta CLP, usar la primera disponible
        account = Account.objects.filter(user=request.user).first()

    if account is None:
        messages.error(request, 'No tienes cuentas activas. Contacta al administrador.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            # Crear la transacción de depósito (sender=None indica origen externo)
            Transaction.objects.create(
                sender_account=None,
                receiver_account=account,
                amount=amount,
            )

            # Actualizar el balance de la cuenta
            account.deposit(amount)

            messages.success(
                request,
                f'Depósito de {account.currency.currency_symbol} '
                f'{amount:,.2f} realizado correctamente.'
            )
            return redirect('dashboard')

        messages.error(request, 'Por favor ingresa un monto válido.')
    else:
        form = DepositForm()

    context = {
        'form': form,
        'account': account,
    }
    return render(request, 'wallet/deposit.html', context)
