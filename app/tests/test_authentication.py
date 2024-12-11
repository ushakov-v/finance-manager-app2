# app_name/tests/test_authentication.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserAuthenticationTests(TestCase):

    def test_registration(self):
        """Тестирование регистрации нового пользователя"""
        data = {'username': 'testuser', 'email': 'testuser@example.com', 'password1': 'password123', 'password2': 'password123'}
        response = self.client.post(reverse('register'), data)
        self.assertRedirects(response, reverse('transaction_list'))  # Перенаправление на страницу с транзакциями
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Проверка, что пользователь создан

    def test_login(self):
        """Тестирование входа в систему"""
        user = User.objects.create_user(username='testuser', password='password123')
        data = {'username': 'testuser', 'password': 'password123'}
        response = self.client.post(reverse('login'), data)
        self.assertRedirects(response, reverse('transaction_list'))  # Перенаправление на страницу с транзакциями

    def test_logout(self):
        """Тестирование выхода из системы"""
        user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))  # Перенаправление на страницу логина
        self.assertNotIn('_auth_user_id', self.client.session)  # Проверка, что пользователь вышел
