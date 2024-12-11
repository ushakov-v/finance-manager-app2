from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from finance_manager_app.models import Transaction
from datetime import datetime

class TransactionViewTests(TestCase):

    def setUp(self):
        """Создаем тестового пользователя и данные для тестов"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_transaction_list_view(self):
        """Тестируем отображение списка транзакций"""
        transaction = Transaction.objects.create(
            transaction_type='income',
            amount=100.00,
            description='Test income',
            user=self.user,
            date=datetime.now()  # Указываем текущую дату
        )
        response = self.client.get(reverse('transaction_list'))  # Делаем GET-запрос на список транзакций
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test income')  # Проверяем, что транзакция отображается

    def test_add_transaction_view(self):
        """Тестируем добавление транзакции"""
        data = {
            'amount': 100.00,
            'transaction_type': 'income',
            'description': 'Test income',
            'date': datetime.now().strftime('%Y-%m-%d')  # Указываем текущую дату в правильном формате
        }
        response = self.client.post(reverse('add_transaction'), data)
        self.assertRedirects(response, reverse('transaction_list'))  # Перенаправление на страницу с транзакциями
        self.assertTrue(Transaction.objects.filter(description='Test income').exists())  # Проверка, что транзакция добавлена

    def test_edit_transaction_view(self):
        """Тестируем редактирование транзакции"""
        transaction = Transaction.objects.create(
            transaction_type='income',
            amount=100.00,
            description='Old income',
            user=self.user,
            date=datetime.now()  # Указываем дату
        )
        data = {
            'amount': 150.00,
            'transaction_type': 'income',
            'description': 'Updated income',
            'date': datetime.now().strftime('%Y-%m-%d')  # Указываем дату
        }
        response = self.client.post(reverse('edit_transaction', kwargs={'pk': transaction.pk}), data)
        self.assertRedirects(response, reverse('transaction_list'))  # Перенаправление на страницу с транзакциями
        transaction.refresh_from_db()  # Обновляем объект из базы данных
        self.assertEqual(transaction.description, 'Updated income')  # Проверка, что описание обновлено

    def test_delete_transaction_view(self):
        """Тестируем удаление транзакции"""
        transaction = Transaction.objects.create(
            transaction_type='income',
            amount=100.00,
            description='Test income',
            user=self.user,
            date=datetime.now()  # Указываем дату
        )
        response = self.client.post(reverse('delete_transaction', kwargs={'pk': transaction.pk}))
        self.assertRedirects(response, reverse('transaction_list'))  # Перенаправление на страницу с транзакциями
        self.assertFalse(Transaction.objects.filter(pk=transaction.pk).exists())  # Проверка, что транзакция удалена
