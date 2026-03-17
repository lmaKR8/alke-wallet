"""Tests de la app contacts — búsqueda de contactos y envío de dinero."""

from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.transactions.models import Transaction
from apps.wallet.models import Account

User = get_user_model()


class ContactsTest(TestCase):
    """Tests de integración para las vistas de contactos y envío de dinero."""

    fixtures = ['currencies', 'users', 'accounts']

    def setUp(self):
        self.client = Client()
        self.client.login(username='frodo.bolson@shire.me', password='password123')
        # Frodo (pk=1) → remitente; Bilbo (pk=2) → receptor
        self.receiver = User.objects.get(pk=2)
        self.sender_account = Account.objects.filter(
            user__email='frodo.bolson@shire.me',
            currency__currency_symbol='CLP',
        ).first()
        self.receiver_account = Account.objects.filter(
            user=self.receiver,
            currency__currency_symbol='CLP',
        ).first()

    def test_contacts_list_search(self):
        """Verifica que GET /contacts/?q=bilbo retorna resultados filtrados."""
        response = self.client.get(reverse('contact_list'), {'q': 'bilbo'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bilbo')

    def test_send_money_success(self):
        """Verifica que un POST válido crea la Transaction y actualiza los balances."""
        balance_sender_before = self.sender_account.balance
        balance_receiver_before = self.receiver_account.balance
        tx_count_before = Transaction.objects.count()

        self.client.post(
            reverse('send_money', kwargs={'receiver_id': self.receiver.pk}),
            {'amount': '100.00', 'message': 'Test'},
        )

        self.sender_account.refresh_from_db()
        self.receiver_account.refresh_from_db()
        self.assertEqual(Transaction.objects.count(), tx_count_before + 1)
        self.assertEqual(self.sender_account.balance, balance_sender_before - Decimal('100.00'))
        self.assertEqual(self.receiver_account.balance, balance_receiver_before + Decimal('100.00'))

    def test_send_money_insufficient_funds(self):
        """Verifica que enviar más saldo del disponible no crea Transaction."""
        tx_count_before = Transaction.objects.count()
        response = self.client.post(
            reverse('send_money', kwargs={'receiver_id': self.receiver.pk}),
            {'amount': '999999999.00', 'message': ''},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Transaction.objects.count(), tx_count_before)

    def test_send_money_atomic(self):
        """Verifica que un fallo en receiver.deposit() hace rollback de toda la transacción."""
        tx_count_before = Transaction.objects.count()
        with patch.object(Account, 'deposit', side_effect=Exception('Fallo simulado')):
            self.client.post(
                reverse('send_money', kwargs={'receiver_id': self.receiver.pk}),
                {'amount': '100.00', 'message': ''},
            )
        self.assertEqual(Transaction.objects.count(), tx_count_before)
