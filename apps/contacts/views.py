"""
Vistas CRUD de contactos y envío de dinero.

my_contacts_view  — lista de contactos propios con búsqueda (GET)
add_contact_view  — buscar usuarios y guardarlos como contacto (GET/POST)
edit_contact_view — editar alias de un contacto (GET/POST)
delete_contact_view — eliminar un contacto (POST)
send_money_view   — transferencia atómica a otro usuario (GET/POST)
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.models import User
from apps.contacts.forms import ContactAliasForm, SendMoneyForm
from apps.contacts.models import Contact
from apps.transactions.models import Transaction
from apps.wallet.models import Account


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_sender_account(user):
    """Devuelve la cuenta CLP del usuario, o la primera disponible."""
    account = Account.objects.filter(
        user=user, currency__currency_symbol='CLP'
    ).first()
    if account is None:
        account = Account.objects.filter(user=user).first()
    return account


# ---------------------------------------------------------------------------
# CRUD de contactos
# ---------------------------------------------------------------------------

@login_required
def my_contacts_view(request):
    """
    Lista de contactos del usuario autenticado.

    Muestra el saldo disponible, un buscador (por nombre o alias) y las
    tarjetas de cada contacto con botones de enviar / editar / eliminar.
    """
    search_term = request.GET.get('q', '').strip()

    qs = Contact.objects.filter(owner=request.user).select_related('contact_user')

    if search_term:
        qs = qs.filter(
            Q(alias__icontains=search_term) |
            Q(contact_user__user_name__icontains=search_term) |
            Q(contact_user__email__icontains=search_term)
        )

    sender_account = _get_sender_account(request.user)

    return render(request, 'contacts/list.html', {
        'contacts': qs,
        'search_term': search_term,
        'sender_account': sender_account,
    })


@login_required
def add_contact_view(request):
    """
    Busca usuarios del sistema (GET con ?q=) y guarda uno como contacto (POST).
    """
    search_term = request.GET.get('q', '').strip()

    # IDs de contactos ya guardados
    existing_ids = Contact.objects.filter(
        owner=request.user
    ).values_list('contact_user_id', flat=True)

    users = (
        User.objects.exclude(id=request.user.id)
        .exclude(id__in=existing_ids)
        .order_by('user_name')
    )

    if search_term:
        users = users.filter(
            Q(user_name__icontains=search_term) |
            Q(email__icontains=search_term)
        )

    if request.method == 'POST':
        contact_user_id = request.POST.get('contact_user_id')
        form = ContactAliasForm(request.POST)

        if not contact_user_id:
            messages.error(request, 'Debes seleccionar un usuario.')
            return redirect('add_contact')

        contact_user = get_object_or_404(User, id=contact_user_id)

        if contact_user == request.user:
            messages.error(request, 'No puedes agregarte a ti mismo como contacto.')
            return redirect('add_contact')

        if form.is_valid():
            alias = form.cleaned_data.get('alias', '').strip()
            _, created = Contact.objects.get_or_create(
                owner=request.user,
                contact_user=contact_user,
                defaults={'alias': alias},
            )
            if created:
                messages.success(
                    request,
                    f'{contact_user.user_name} agregado a tus contactos.'
                )
            else:
                messages.info(
                    request,
                    f'{contact_user.user_name} ya estaba en tus contactos.'
                )
            return redirect('contact_list')

    return render(request, 'contacts/add_contact.html', {
        'users': users,
        'search_term': search_term,
        'form': ContactAliasForm(),
    })


@login_required
def edit_contact_view(request, pk):
    """Edita el alias de un contacto existente."""
    contact = get_object_or_404(Contact, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = ContactAliasForm(request.POST)
        if form.is_valid():
            contact.alias = form.cleaned_data.get('alias', '').strip()
            contact.save()
            messages.success(request, 'Alias actualizado correctamente.')
            return redirect('contact_list')
    else:
        form = ContactAliasForm(initial={'alias': contact.alias})

    return render(request, 'contacts/edit_contact.html', {
        'contact': contact,
        'form': form,
    })


@login_required
def delete_contact_view(request, pk):
    """Elimina un contacto (solo acepta POST)."""
    contact = get_object_or_404(Contact, pk=pk, owner=request.user)

    if request.method == 'POST':
        name = contact.display_name
        contact.delete()
        messages.success(request, f'{name} eliminado de tus contactos.')

    return redirect('contact_list')


# ---------------------------------------------------------------------------
# Envío de dinero
# ---------------------------------------------------------------------------

@login_required
def send_money_view(request, receiver_id):
    """
    Vista para enviar dinero a otro usuario (transferencia atómica).

    GET:  Muestra el formulario de envío.
    POST: Realiza la transferencia usando transaction.atomic().
    """
    receiver = get_object_or_404(User, id=receiver_id)

    if receiver == request.user:
        messages.error(request, 'No puedes enviarte dinero a ti mismo.')
        return redirect('contact_list')

    sender_account = _get_sender_account(request.user)

    if sender_account is None:
        messages.error(request, 'No tienes cuentas activas para realizar envíos.')
        return redirect('dashboard')

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

    # Alias del receptor (si está guardado como contacto)
    contact_obj = Contact.objects.filter(
        owner=request.user, contact_user=receiver
    ).first()

    if request.method == 'POST':
        form = SendMoneyForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']

            if amount > sender_account.balance:
                messages.error(
                    request,
                    f'Saldo insuficiente. Tu saldo es '
                    f'{sender_account.currency.currency_symbol} '
                    f'{sender_account.balance:,.2f}.'
                )
                return render(request, 'contacts/send_money.html', {
                    'form': form,
                    'receiver': receiver,
                    'sender_account': sender_account,
                    'receiver_account': receiver_account,
                    'contact_obj': contact_obj,
                })

            try:
                with transaction.atomic():
                    Transaction.objects.create(
                        sender_account=sender_account,
                        receiver_account=receiver_account,
                        amount=amount,
                    )
                    sender_account.withdraw(amount)
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

    return render(request, 'contacts/send_money.html', {
        'form': form,
        'receiver': receiver,
        'sender_account': sender_account,
        'receiver_account': receiver_account,
        'contact_obj': contact_obj,
    })
