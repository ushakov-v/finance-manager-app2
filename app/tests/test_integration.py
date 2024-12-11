from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from finance_manager_app.models import Transaction
from django.utils import timezone


class TransactionFormIntegrationTestCase(TestCase):

    def setUp(self):
        """Создание пользователя и вход в систему"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_transaction_integration(self):
        """Тестируем создание транзакции через форму"""
        # Данные формы для добавления транзакции
        form_data = {
            'transaction_type': 'income',  # Тип транзакции (доход)
            'amount': 200,  # Сумма
            'date': '2024-12-10',  # Дата
            'description': 'Test income transaction',  # Описание
            'category_income': 'salary'  # Категория (доход)
        }

        # Отправляем POST-запрос для создания транзакции
        response = self.client.post(reverse('add_transaction'), data=form_data)

        # Проверка, что редирект произошел на страницу транзакций
        self.assertEqual(response.status_code, 302)  # 302 - редирект
        self.assertRedirects(response, reverse('transaction_list'))

        # Проверка, что транзакция была добавлена в базу данных
        transaction = Transaction.objects.get(description='Test income transaction')
        self.assertEqual(transaction.amount, 200)
        self.assertEqual(transaction.transaction_type, 'income')

        # Проверка, что транзакция появилась на странице списка транзакций
        response = self.client.get(reverse('transaction_list'))
        self.assertContains(response, 'Test income transaction')
        self.assertContains(response, '200')
        self.assertContains(response, 'Доход')

    def test_create_transaction_invalid_data(self):
        """Проверка обработки некорректных данных в форме"""
        # Некорректные данные (неверная сумма)
        form_data = {
            'transaction_type': 'income',
            'amount': 'invalid',  # Некорректная сумма
            'date': '2024-12-10',
            'description': 'Invalid income transaction',
            'category_income': 'salary'
        }

        # Отправляем некорректные данные
        response = self.client.post(reverse('add_transaction'), data=form_data)

        # Проверка, что форма не прошла валидацию и возвращает ошибки
        self.assertFormError(response, 'form', 'amount', 'Введите число.')

    def test_transaction_list_page(self):
        """Проверка, что список транзакций отображается корректно"""

        # Создаем несколько транзакций, связывая их с пользователем
        Transaction.objects.create(
            user=self.user,  # Указываем пользователя
            transaction_type='income',
            amount=100.00,
            date=timezone.now(),
            description='Test income',
            category_income='salary'
        )

        Transaction.objects.create(
            user=self.user,  # Указываем пользователя
            transaction_type='expense',
            amount=50.00,
            date=timezone.now(),
            description='Test expense',
            category_expense='food'
        )

        # URL страницы списка транзакций
        url = reverse('transaction_list')

        # Получаем страницу списка транзакций
        response = self.client.get(url)

        # Проверяем, что страница загружена успешно
        self.assertEqual(response.status_code, 200)

        # Проверяем, что транзакции отображаются на странице
        self.assertContains(response, 'Test income')
        self.assertContains(response, 'Test expense')

        # Проверяем, что транзакции относятся к текущему пользователю
        transactions = response.context['transactions']
        for transaction in transactions:
            self.assertEqual(transaction.user, self.user)


    def test_transaction_edit_functionality(self):
        """Проверка функциональности редактирования транзакции"""
        # Создаем транзакцию, связываем с пользователем
        transaction = Transaction.objects.create(
            user=self.user,  # Указываем пользователя
            transaction_type='income',
            amount=100,
            date=timezone.now(),
            description='Transaction to edit',
            category_income='salary'
        )

        # URL для редактирования транзакции
        edit_url = reverse('edit_transaction', args=[transaction.pk])

        # Данные для редактирования транзакции
        data = {
            'transaction_type': 'income',  # Оставляем тот же тип
            'amount': 200,  # Меняем сумму
            'date': timezone.now().date(),  # Меняем дату (или оставляем текущую)
            'description': 'Updated transaction',  # Обновляем описание
            'category_income': 'salary'  # Оставляем категорию дохода
        }

        # Отправляем запрос с изменениями
        response = self.client.post(edit_url, data)

        # Проверка, что редирект произошел на страницу со списком транзакций
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('transaction_list'))

        # Проверка, что транзакция была обновлена
        transaction.refresh_from_db()  # Перезагружаем объект из базы данных
        self.assertEqual(transaction.amount, 200)
        self.assertEqual(transaction.description, 'Updated transaction')


    def test_transaction_delete_functionality(self):
        """Проверка функциональности удаления транзакции"""
        # Создаем транзакцию для удаления, связываем с пользователем
        transaction = Transaction.objects.create(
            user=self.user,  # Здесь указываем пользователя, который создает транзакцию
            transaction_type='expense',
            amount=50,
            date=timezone.now(),
            description='Transaction to delete',
            category_expense='food'
        )

        # Отправляем запрос на удаление транзакции
        response = self.client.post(reverse('delete_transaction', args=[transaction.pk]))

        # Проверка, что редирект произошел на страницу списка транзакций
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('transaction_list'))

        # Проверка, что транзакция была удалена из базы данных
        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(pk=transaction.pk)

