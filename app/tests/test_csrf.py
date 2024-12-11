# app/tests/test_csrf.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class CSRFProtectionTests(TestCase):

    def test_csrf_token_required_for_anonymous_user(self):
        """Проверка, что анонимный пользователь будет перенаправлен при попытке отправить форму без CSRF-токена"""
        response = self.client.post(reverse('add_transaction'), {'amount': 100.00, 'transaction_type': 'income'})

        # Проверяем, что анонимный пользователь был перенаправлен на страницу входа (код 302)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/add/')

    def test_csrf_token_required_for_authenticated_user(self):
        """Проверка, что аутентифицированный пользователь получает ошибку 403 при отправке запроса без CSRF-токена"""
        # Создаем аутентифицированного пользователя
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Отправляем POST-запрос без CSRF-токена
        response = self.client.post(reverse('add_transaction'), {'amount': 100.00, 'transaction_type': 'income'},
                                    follow=False)

        # Проверяем, что запрос без CSRF-токена вызывает ошибку 403
        self.assertEqual(response.status_code, 403)
