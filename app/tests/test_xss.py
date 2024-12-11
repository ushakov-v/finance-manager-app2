from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from finance_manager_app.models import Transaction
from datetime import datetime

class XSSProtectionTests(TestCase):

    def setUp(self):
        """Создаем тестового пользователя и данные для тестов"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_xss_prevention(self):
        """Проверка, что пользовательские данные экранируются для предотвращения XSS-атак"""
        # Данные с XSS-скриптом
        data = {
            'amount': 100.00,
            'transaction_type': 'income',
            'description': '<script>alert("XSS")</script>',
            'date': datetime.now().strftime('%Y-%m-%d')  # Указываем дату
        }

        # Отправляем форму для добавления транзакции
        response = self.client.post(reverse('add_transaction'), data)

        # Поскольку происходит перенаправление, выполняем GET-запрос на страницу, куда идет редирект
        # В случае успешного добавления, редиректит на 'transaction_list'
        self.assertRedirects(response, reverse('transaction_list'))

        # Теперь выполняем GET-запрос на страницу списка транзакций
        response = self.client.get(reverse('transaction_list'))

        # Проверяем, что вредоносный скрипт не исполнился и не отображается как HTML
        self.assertNotContains(response, '<script>alert("XSS")</script>')
