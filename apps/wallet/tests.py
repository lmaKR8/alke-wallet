"""Tests de la app wallet — modelos Account + Currency, vistas dashboard y depósito."""

from decimal import Decimal

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.transactions.models import Transaction
from apps.wallet.models import Account

User = get_user_model()


class WalletTest(TestCase):
    """Tests del modelo Account, soft delete y vistas wallet."""

    fixtures = ['currencies', 'users', 'accounts']

    def setUp(self):
        self.client = Client()
        self.client.login(username='frodo.bolson@shire.me', password='password123')
        self.account = Account.objects.filter(
            user__email='frodo.bolson@shire.me',
            currency__currency_symbol='CLP',
        ).first()

    def test_deposit_creates_transaction(self):
        """Verifica que POST /deposit/ crea una Transaction con sender_account=None."""
        count_before = Transaction.objects.count()
        self.client.post(reverse('deposit'), {'amount': '1000.00'})
        self.assertEqual(Transaction.objects.count(), count_before + 1)
        tx = Transaction.objects.latest('transaction_date')
        self.assertIsNone(tx.sender_account)

    def test_deposit_updates_balance(self):
        """Verifica que POST /deposit/ incrementa el balance de la cuenta."""
        balance_before = Account.objects.get(pk=self.account.pk).balance
        self.client.post(reverse('deposit'), {'amount': '500.00'})
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, balance_before + Decimal('500.00'))

    def test_deposit_invalid_amount(self):
        """Verifica que POST /deposit/ con monto=0 no crea ninguna Transaction."""
        count_before = Transaction.objects.count()
        self.client.post(reverse('deposit'), {'amount': '0'})
        self.assertEqual(Transaction.objects.count(), count_before)

    def test_soft_delete_account(self):
        """Verifica que soft_delete() establece deleted_at en la cuenta."""
        self.account.soft_delete()
        self.assertIsNotNone(self.account.deleted_at)

    def test_soft_delete_excludes_from_queryset(self):
        """Verifica que Account.objects.all() no incluye cuentas con soft delete."""
        pk = self.account.pk
        self.account.soft_delete()
        self.assertFalse(Account.objects.filter(pk=pk).exists())

    def test_dashboard_requires_login(self):
        """Verifica que GET /dashboard/ sin sesión redirige al login."""
        client = Client()
        response = client.get(reverse('dashboard'))
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('dashboard')}",
            fetch_redirect_response=False,
        )

