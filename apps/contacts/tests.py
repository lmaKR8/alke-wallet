"""Tests de la app contacts — CRUD de contactos y envío de dinero."""

from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.contacts.models import Contact
from apps.transactions.models import Transaction
from apps.wallet.models import Account

User = get_user_model()


class MyContactsCRUDTest(TestCase):
    """Tests del CRUD de contactos propios (my_contacts_view y acciones)."""

    fixtures = ['currencies', 'users', 'accounts']

    def setUp(self):
        self.client = Client()
        self.client.login(username='frodo.bolson@shire.me', password='password123')
        self.bilbo = User.objects.get(pk=2)
        self.frodo = User.objects.get(email='frodo.bolson@shire.me')

    # --- LIST ---

    def test_contacts_list_empty(self):
        """Sin contactos, la vista carga sin errores."""
        response = self.client.get(reverse('contact_list'))
        self.assertEqual(response.status_code, 200)

    def test_contacts_list_shows_contacts(self):
        """Los contactos guardados aparecen en la lista."""
        Contact.objects.create(owner=self.frodo, contact_user=self.bilbo, alias='El tío')
        response = self.client.get(reverse('contact_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bilbo')

    def test_contacts_list_search_by_alias(self):
        """La búsqueda filtra por alias."""
        Contact.objects.create(owner=self.frodo, contact_user=self.bilbo, alias='El tío')
        response = self.client.get(reverse('contact_list'), {'q': 'tío'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bilbo')

    def test_contacts_list_search_by_name(self):
        """La búsqueda filtra por nombre de usuario del contacto."""
        Contact.objects.create(owner=self.frodo, contact_user=self.bilbo, alias='')
        response = self.client.get(reverse('contact_list'), {'q': 'bilbo'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bilbo')

    # --- ADD ---

    def test_add_contact_get(self):
        """GET /contacts/add/ responde 200."""
        response = self.client.get(reverse('add_contact'))
        self.assertEqual(response.status_code, 200)

    def test_add_contact_search(self):
        """GET /contacts/add/?q=bilbo muestra resultados de búsqueda."""
        response = self.client.get(reverse('add_contact'), {'q': 'bilbo'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bilbo')

    def test_add_contact_post_creates_contact(self):
        """POST crea un nuevo contacto y redirige a contact_list."""
        self.assertEqual(Contact.objects.filter(owner=self.frodo).count(), 0)
        response = self.client.post(
            reverse('add_contact'),
            {'contact_user_id': self.bilbo.pk, 'alias': 'El tío'},
        )
        self.assertRedirects(response, reverse('contact_list'))
        self.assertEqual(Contact.objects.filter(owner=self.frodo).count(), 1)
        c = Contact.objects.get(owner=self.frodo, contact_user=self.bilbo)
        self.assertEqual(c.alias, 'El tío')

    def test_add_contact_post_no_duplicate(self):
        """No se puede agregar el mismo contacto dos veces."""
        Contact.objects.create(owner=self.frodo, contact_user=self.bilbo, alias='')
        self.client.post(
            reverse('add_contact'),
            {'contact_user_id': self.bilbo.pk, 'alias': 'Otro alias'},
        )
        self.assertEqual(Contact.objects.filter(owner=self.frodo, contact_user=self.bilbo).count(), 1)

    # --- EDIT ---

    def test_edit_contact_get(self):
        """GET /contacts/<pk>/edit/ responde 200."""
        c = Contact.objects.create(owner=self.frodo, contact_user=self.bilbo, alias='Viejo')
        response = self.client.get(reverse('edit_contact', kwargs={'pk': c.pk}))
        self.assertEqual(response.status_code, 200)

    def test_edit_contact_post_updates_alias(self):
        """POST actualiza el alias y redirige."""
        c = Contact.objects.create(owner=self.frodo, contact_user=self.bilbo, alias='Viejo')
        response = self.client.post(
            reverse('edit_contact', kwargs={'pk': c.pk}),
            {'alias': 'Nuevo alias'},
        )
        self.assertRedirects(response, reverse('contact_list'))
        c.refresh_from_db()
        self.assertEqual(c.alias, 'Nuevo alias')

    # --- DELETE ---

    def test_delete_contact_post_removes_contact(self):
        """POST elimina el contacto y redirige."""
        c = Contact.objects.create(owner=self.frodo, contact_user=self.bilbo, alias='')
        response = self.client.post(reverse('delete_contact', kwargs={'pk': c.pk}))
        self.assertRedirects(response, reverse('contact_list'))
        self.assertFalse(Contact.objects.filter(pk=c.pk).exists())

    def test_delete_contact_other_user_forbidden(self):
        """No se puede eliminar un contacto ajeno."""
        gandalf = User.objects.exclude(email='frodo.bolson@shire.me').first()
        c = Contact.objects.create(owner=gandalf, contact_user=self.bilbo, alias='')
        response = self.client.post(reverse('delete_contact', kwargs={'pk': c.pk}))
        # Debe devolver 404 (get_object_or_404 con owner=request.user)
        self.assertEqual(response.status_code, 404)


class SendMoneyTest(TestCase):
    """Tests de integración para la vista de envío de dinero."""

    fixtures = ['currencies', 'users', 'accounts']

    def setUp(self):
        self.client = Client()
        self.client.login(username='frodo.bolson@shire.me', password='password123')
        self.receiver = User.objects.get(pk=2)
        self.sender_account = Account.objects.filter(
            user__email='frodo.bolson@shire.me',
            currency__currency_symbol='CLP',
        ).first()
        self.receiver_account = Account.objects.filter(
            user=self.receiver,
            currency__currency_symbol='CLP',
        ).first()

    def test_send_money_success(self):
        """Un POST válido crea la Transaction y actualiza los balances."""
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
        """Enviar más saldo del disponible no crea Transaction."""
        tx_count_before = Transaction.objects.count()
        response = self.client.post(
            reverse('send_money', kwargs={'receiver_id': self.receiver.pk}),
            {'amount': '999999999.00', 'message': ''},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Transaction.objects.count(), tx_count_before)

    def test_send_money_atomic(self):
        """Un fallo en receiver.deposit() hace rollback de toda la transacción."""
        tx_count_before = Transaction.objects.count()
        with patch.object(Account, 'deposit', side_effect=Exception('Fallo simulado')):
            self.client.post(
                reverse('send_money', kwargs={'receiver_id': self.receiver.pk}),
                {'amount': '100.00', 'message': ''},
            )
        self.assertEqual(Transaction.objects.count(), tx_count_before)
