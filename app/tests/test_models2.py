from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from finance_manager_app.models import Transaction  # Замените на актуальное имя вашего приложения


class TransactionModelTestCase(TestCase):

    def setUp(self):
        """Создание пользователя для тестов"""
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.transaction = Transaction(
            user=self.user,
            transaction_type='income',
            amount=100.50,
            date=date(2024, 12, 1),
            description='Test income transaction',
            category_income='salary'
        )
        self.transaction.save()  # Сохраняем транзакцию вручную

    def test_transaction_creation(self):
        """Проверка правильности создания транзакции"""
        transaction = self.transaction
        self.assertEqual(transaction.transaction_type, 'income')
        self.assertEqual(transaction.amount, 100.50)
        self.assertEqual(transaction.date, date(2024, 12, 1))
        self.assertEqual(transaction.description, 'Test income transaction')
        self.assertEqual(transaction.category_income, 'salary')
        self.assertIsNone(transaction.category_expense)  # Для income категория расхода не должна быть задана

    def test_str_method(self):
        """Проверка работы метода __str__"""
        transaction = self.transaction
        expected_str = 'Income - 100.5 - 2024-12-01'
        self.assertEqual(str(transaction), expected_str)

    def test_category_expense_for_income(self):
        """Проверка, что для доходов категория расхода не может быть задана"""
        self.transaction.category_expense = 'food'
        self.transaction.save()
        self.assertIsNone(self.transaction.category_expense)

    def test_category_income_for_expense(self):
        """Проверка, что для расходов категория дохода не может быть задана"""
        self.transaction.transaction_type = 'expense'
        self.transaction.category_income = 'salary'  # Это неверно для расходов
        self.transaction.save()
        self.assertIsNone(self.transaction.category_income)

    def test_transaction_amount_validation(self):
        """Проверка, что сумма транзакции положительная"""
        invalid_transaction = Transaction(
            user=self.user,
            transaction_type='expense',
            amount=-50.00,  # Невалидная сумма
            date=date(2024, 12, 2),
            description='Invalid expense',
        )
        with self.assertRaises(ValueError):
            invalid_transaction.save()

    def test_transaction_description_length(self):
        """Проверка длины описания"""
        long_description = 'a' * 256  # Превышаем максимально допустимую длину
        transaction = Transaction(
            user=self.user,
            transaction_type='income',
            amount=200.00,
            date=date(2024, 12, 1),
            description=long_description,  # Должно вызвать ошибку
        )
        with self.assertRaises(ValueError):
            transaction.save()
