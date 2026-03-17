"""
Vista del historial de transacciones con filtros dinámicos (Model Q) y paginación.

Implementa el patrón de filtros dinámicos de:
fuente-verdad/django_docs/uso de model Q en Django.md
"""

from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.shortcuts import render
from django.utils import timezone

from apps.transactions.models import Transaction


@login_required
def transaction_list_view(request):
    """
    Vista del historial de transacciones del usuario autenticado.

    Obtiene todas las transacciones donde el usuario es remitente o receptor,
    aplica filtros por tipo y período usando Model Q, calcula totales
    y pagina los resultados.

    Parámetros GET:
        tipo (str): 'todos' | 'deposito' | 'envio' | 'recibido'
        periodo (str): '7' | '30' | '90' | '365' (días hacia atrás)
        page (int): Número de página para la paginación.

    Args:
        request: El objeto HttpRequest de Django.

    Returns:
        HttpResponse: Template con lista paginada y filtros aplicados.
    """
    # Obtener parámetros de filtro con valores por defecto
    tipo = request.GET.get('tipo', 'todos')
    periodo = request.GET.get('periodo', '90')

    # --- Construir query base con Model Q ---
    # Obtener transacciones donde el usuario es remitente o receptor
    user_accounts_ids = request.user.accounts.values_list('id', flat=True)

    base_query = Q(sender_account_id__in=user_accounts_ids) | \
                 Q(receiver_account_id__in=user_accounts_ids)

    # --- Filtro por tipo usando Model Q ---
    if tipo == 'deposito':
        # Depósitos: sender_account es NULL y el receptor es el usuario
        tipo_query = Q(sender_account__isnull=True) & \
                     Q(receiver_account_id__in=user_accounts_ids)
    elif tipo == 'envio':
        # Envíos: el remitente es el usuario (sender no es NULL)
        tipo_query = Q(sender_account_id__in=user_accounts_ids) & \
                     Q(sender_account__isnull=False)
    elif tipo == 'recibido':
        # Recibidos: el receptor es el usuario y hay un remitente real
        tipo_query = Q(receiver_account_id__in=user_accounts_ids) & \
                     Q(sender_account__isnull=False)
    else:
        # 'todos': cualquier transacción del usuario
        tipo_query = base_query

    # --- Filtro por período ---
    try:
        dias = int(periodo)
    except (ValueError, TypeError):
        dias = 30

    fecha_inicio = timezone.now() - timedelta(days=dias)
    periodo_query = Q(transaction_date__gte=fecha_inicio)

    # --- Consulta final optimizada con select_related ---
    transactions = Transaction.objects.filter(
        tipo_query & periodo_query
    ).select_related(
        'sender_account__user',
        'sender_account__currency',
        'receiver_account__user',
        'receiver_account__currency',
    ).order_by('-transaction_date').distinct()

    # --- Calcular totales de ingresos y egresos ---
    depositos_ids = transactions.filter(
        sender_account__isnull=True,
        receiver_account_id__in=user_accounts_ids,
    ).values_list('id', flat=True)

    recibidos_ids = transactions.filter(
        sender_account__isnull=False,
        receiver_account_id__in=user_accounts_ids,
    ).values_list('id', flat=True)

    envios_ids = transactions.filter(
        sender_account_id__in=user_accounts_ids,
        sender_account__isnull=False,
    ).values_list('id', flat=True)

    total_ingresos = Transaction.objects.filter(
        id__in=list(depositos_ids) + list(recibidos_ids)
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_egresos = Transaction.objects.filter(
        id__in=list(envios_ids)
    ).aggregate(total=Sum('amount'))['total'] or 0

    # --- Paginación (5 items por página) ---
    paginator = Paginator(transactions, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'tipo_seleccionado': tipo,
        'periodo_seleccionado': periodo,
        'total_ingresos': total_ingresos,
        'total_egresos': total_egresos,
        'user_accounts_ids': list(user_accounts_ids),
    }
    return render(request, 'transactions/list.html', context)
