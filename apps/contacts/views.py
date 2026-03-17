"""
Vistas de la app contacts — búsqueda de usuarios y envío de dinero.

Implementa búsqueda con Model Q y transferencias atómicas con transaction.atomic().
Patrones de fuente-verdad/django_docs/uso de model Q en Django.md
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.models import User
from apps.contacts.forms import SendMoneyForm
from apps.transactions.models import Transaction
from apps.wallet.models import Account


@login_required
def contacts_view(request):
    """
    Vista de búsqueda de contactos (otros usuarios del sistema).

    Permite buscar usuarios por nombre o email usando Model Q para
    construir un filtro dinámico con OR. Excluye al usuario autenticado
    de los resultados.

    Parámetros GET:
        q (str): Término de búsqueda (nombre o email).

    Args:
        request: El objeto HttpRequest de Django.

    Returns:
        HttpResponse: Lista filtrada de usuarios con opción de enviar dinero.
    """
    search_term = request.GET.get('q', '').strip()

    if search_term:
        # Patrón Model Q: filtro dinámico con OR
        search_query = (
            Q(user_name__icontains=search_term) |
            Q(email__icontains=search_term)
        )
        users = User.objects.filter(search_query).exclude(
            id=request.user.id
        ).order_by('user_name')
    else:
        # Sin búsqueda: mostrar todos los demás usuarios
        users = User.objects.exclude(id=request.user.id).order_by('user_name')

    context = {
        'users': users,
        'search_term': search_term,
    }
    return render(request, 'contacts/list.html', context)


@login_required
def send_money_view(request, receiver_id):
    """
    Vista para enviar dinero a otro usuario (transferencia atómica).

    GET: Muestra el formulario de envío con información del receptor.
    POST: Realiza la transferencia de forma atómica usando transaction.atomic():
        1. Valida que el monto es positivo y que hay saldo suficiente.
        2. Crea la Transaction.
        3. Descuenta el balance del sender.
        4. Incrementa el balance del receiver.
        Si cualquier paso falla, se hace rollback completo.

    Args:
        request: El objeto HttpRequest de Django.
        receiver_id (int): ID del usuario receptor.

    Returns:
        HttpResponse: Formulario de envío o redirección al dashboard.
    """
    receiver = get_object_or_404(User, id=receiver_id)

    # Verificar que no se envía dinero a sí mismo
    if receiver == request.user:
        messages.error(request, 'No puedes enviarte dinero a ti mismo.')
        return redirect('contact_list')

    # Obtener cuenta principal CLP del sender
    sender_account = Account.objects.filter(
        user=request.user,
        currency__currency_symbol='CLP',
    ).first()

    if sender_account is None:
        sender_account = Account.objects.filter(user=request.user).first()

    if sender_account is None:
        messages.error(request, 'No tienes cuentas activas para realizar envíos.')
        return redirect('dashboard')

    # Obtener cuenta del receptor en la misma moneda
    receiver_account = Account.objects.filter(
        user=receiver,
        currency=sender_account.currency,
    ).first()

    if receiver_account is None:
        messages.error(
            request,
            f'{receiver.user_name} no tiene una cuenta en '
            f'{sender_account.currency.currency_symbol}.'
        )
        return redirect('contact_list')

    if request.method == 'POST':
        form = SendMoneyForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            # Validar saldo suficiente
            if amount > sender_account.balance:
                messages.error(
                    request,
                    f'Saldo insuficiente. Tu saldo es '
                    f'{sender_account.currency.currency_symbol} '
                    f'{sender_account.balance:,.2f}.'
                )
                context = {
                    'form': form,
                    'receiver': receiver,
                    'sender_account': sender_account,
                    'receiver_account': receiver_account,
                }
                return render(request, 'contacts/send_money.html', context)

            # Transferencia atómica: si falla cualquier paso → rollback total
            try:
                with transaction.atomic():
                    # 1. Crear el registro de transacción
                    Transaction.objects.create(
                        sender_account=sender_account,
                        receiver_account=receiver_account,
                        amount=amount,
                    )
                    # 2. Descontar del remitente
                    sender_account.withdraw(amount)
                    # 3. Abonar al receptor
                    receiver_account.deposit(amount)

                messages.success(
                    request,
                    f'Enviaste {sender_account.currency.currency_symbol} '
                    f'{amount:,.2f} a {receiver.user_name} correctamente.'
                )
                return redirect('dashboard')

            except ValueError as e:
                messages.error(request, str(e))
            except Exception:
                messages.error(request, 'Ocurrió un error al procesar la transferencia.')
        else:
            messages.error(request, 'Por favor ingresa un monto válido.')
    else:
        form = SendMoneyForm()

    context = {
        'form': form,
        'receiver': receiver,
        'sender_account': sender_account,
        'receiver_account': receiver_account,
    }
    return render(request, 'contacts/send_money.html', context)
