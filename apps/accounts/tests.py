"""Tests de la app accounts — modelo User y vistas de autenticación."""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountsTest(TestCase):
    """Tests del modelo User y vistas de autenticación."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com',
            user_name='testuser',
            password='TestPass123!',
        )

    def test_user_model_email_login(self):
        """Verifica que el USERNAME_FIELD del modelo User es 'email'."""
        self.assertEqual(User.USERNAME_FIELD, 'email')

    def test_login_valid_credentials(self):
        """Verifica que POST /accounts/login/ con credenciales válidas redirige al dashboard."""
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'TestPass123!',
        })
        self.assertRedirects(
            response,
            reverse('dashboard'),
            fetch_redirect_response=False,
        )

    def test_login_invalid_credentials(self):
        """Verifica que POST /accounts/login/ con credenciales incorrectas devuelve 200."""
        response = self.client.post(reverse('login'), {
            'username': 'test@example.com',
            'password': 'WrongPassword!',
        })
        self.assertEqual(response.status_code, 200)

    def test_register_creates_user(self):
        """Verifica que POST /accounts/register/ crea un nuevo usuario en la BD."""
        response = self.client.post(reverse('register'), {
            'email': 'new@example.com',
            'user_name': 'newuser',
            'password1': 'SecurePass456!',
            'password2': 'SecurePass456!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='new@example.com').exists())

