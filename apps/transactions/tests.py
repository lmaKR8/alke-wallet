"""Tests de la app transactions — vista de historial con filtros y paginación."""

from datetime import timedelta

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class TransactionListViewTest(TestCase):
    """Tests de integración para la vista de lista de transacciones."""

    fixtures = ['currencies', 'users', 'accounts', 'transactions']

    def setUp(self):
        self.client = Client()
        self.client.login(username='frodo.bolson@shire.me', password='password123')

    def test_transaction_list_no_filter(self):
        """Verifica que GET /transactions/ sin filtros devuelve 200 con transacciones del usuario."""
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transactions/list.html')
        self.assertIn('page_obj', response.context)

    def test_transaction_list_filter_type(self):
        """Verifica que GET /transactions/?tipo=envio filtra solo envíos del usuario."""
        response = self.client.get(reverse('transaction_list'), {'tipo': 'envio'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tipo_seleccionado'], 'envio')
        user = response.wsgi_request.user
        user_account_ids = set(user.accounts.values_list('id', flat=True))
        for tx in response.context['page_obj']:
            self.assertIn(tx.sender_account_id, user_account_ids)

    def test_transaction_list_filter_period(self):
        """Verifica que GET /transactions/?periodo=7 filtra los últimos 7 días."""
        response = self.client.get(reverse('transaction_list'), {'periodo': '7'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['periodo_seleccionado'], '7')
        cutoff = timezone.now() - timedelta(days=7)
        for tx in response.context['page_obj']:
            self.assertGreaterEqual(tx.transaction_date, cutoff)

    def test_transaction_list_requires_login(self):
        """Verifica que GET /transactions/ sin sesión redirige al login."""
        client = Client()
        response = client.get(reverse('transaction_list'))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('transaction_list')}",
            fetch_redirect_response=False,
        )
