from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from finance_manager_app.models import Transaction
from django.utils import timezone


class TransactionViewTestCase(TestCase):

    def setUp(self):
        """Создаем пользователя и транзакцию для тестов"""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.transaction = Transaction.objects.create(
            transaction_type='income',
            amount=100,
            date=timezone.now(),
            description='Test transaction',
            user=self.user
        )
        self.client.login(username='testuser', password='password')

    def test_add_transaction_view(self):
        """Тестирование страницы добавления транзакции"""
        url = reverse('add_transaction')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_transaction.html')
        self.assertContains(response, 'Добавить новую транзакцию')

    def test_edit_transaction_view(self):
        """Тестирование страницы редактирования транзакции"""
        url = reverse('edit_transaction', kwargs={'pk': self.transaction.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_transaction.html')
        self.assertContains(response, 'Редактировать транзакцию')

    def test_delete_transaction_view(self):
        """Тестирование страницы удаления транзакции"""
        url = reverse('delete_transaction', kwargs={'pk': self.transaction.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_transaction.html')
        self.assertContains(response, 'Вы уверены, что хотите удалить эту транзакцию?')

    def test_transaction_list_view(self):
        """Тестирование страницы списка транзакций"""
        url = reverse('transaction_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'transaction_list.html')
        self.assertContains(response, 'Мои транзакции')
        self.assertContains(response, 'Test transaction')

    def test_post_add_transaction(self):
        """Тестирование POST-запроса для добавления транзакции"""
        url = reverse('add_transaction')
        data = {
            'transaction_type': 'income',
            'amount': 200,
            'date': '2024-12-01',
            'description': 'New test transaction'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # редирект на страницу с транзакциями
        self.assertTrue(Transaction.objects.filter(description='New test transaction').exists())

    def test_post_edit_transaction(self):
        """Тестирование POST-запроса для редактирования транзакции"""
        url = reverse('edit_transaction', kwargs={'pk': self.transaction.pk})
        data = {
            'transaction_type': 'income',
            'amount': 150,
            'date': '2024-12-01',
            'description': 'Edited transaction'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # редирект на страницу с транзакциями
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.amount, 150)
        self.assertEqual(self.transaction.description, 'Edited transaction')

    def test_post_delete_transaction(self):
        """Тестирование POST-запроса для удаления транзакции"""
        url = reverse('delete_transaction', kwargs={'pk': self.transaction.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # редирект после удаления
        self.assertFalse(Transaction.objects.filter(pk=self.transaction.pk).exists())
