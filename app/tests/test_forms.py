from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from finance_manager_app.forms import TransactionForm
from finance_manager_app.models import Transaction


class TransactionFormTestCase(TestCase):

    def setUp(self):
        """Создаем объект формы для тестов"""
        # Начальные данные для тестирования формы
        self.valid_data = {
            'transaction_type': 'income',
            'amount': Decimal('100.00'),
            'date': timezone.now().date(),
            'description': 'Test income transaction',
            'category_income': 'salary',  # Поставим допустимую категорию дохода
            'category_expense': ''
        }

        self.invalid_data = {
            'transaction_type': 'income',
            'amount': '',
            'date': '',
            'description': 'Test invalid transaction',
            'category_income': '',
            'category_expense': ''
        }

    def test_transaction_form_valid(self):
        """Тестирование валидной формы"""
        form = TransactionForm(data=self.valid_data)
        self.assertTrue(form.is_valid())  # Проверка, что форма валидна

    def test_transaction_form_invalid(self):
        """Тестирование формы с ошибочными данными"""
        form = TransactionForm(data=self.invalid_data)
        self.assertFalse(form.is_valid())  # Форма не должна быть валидной

    def test_transaction_form_field_required(self):
        """Проверка обязательных полей формы"""
        # Передаем данные с пустыми обязательными полями
        form_data = {
            'transaction_type': '',  # Пустое обязательное поле
            'amount': '',  # Пустое обязательное поле
            'date': '',  # Пустое обязательное поле
            'description': '',  # Пустое обязательное поле
            'category_income': '',
            'category_expense': ''
        }
        form = TransactionForm(data=form_data)

        # Проверка, что форма не валидна
        self.assertFalse(form.is_valid())  # Ожидаем, что форма не пройдет валидацию

        # Проверка наличия ошибок для обязательных полей
        self.assertIn('transaction_type', form.errors)
        self.assertIn('amount', form.errors)
        self.assertIn('date', form.errors)
        self.assertIn('description', form.errors)

    def test_category_choices_for_income(self):
        """Проверка наличия выбора категории для доходов"""
        form = TransactionForm(data=self.valid_data)
        category_field = form.fields['category_income']

        # Проверка, что доступные категории содержат правильные варианты
        self.assertIn(('salary', 'Зарплата'), category_field.choices)
        self.assertIn(('other', 'Другие источники'), category_field.choices)

        self.assertTrue(form.is_valid())  # Убедимся, что форма валидна при корректных данных

    def test_category_choices_for_expense(self):
        """Проверка наличия выбора категории для расходов"""

        # Обновим данные для расхода
        expense_data = self.valid_data.copy()
        expense_data['transaction_type'] = 'expense'  # Тип транзакции - расход
        expense_data['category_expense'] = 'food'  # Поставим допустимую категорию расхода

        form = TransactionForm(data=expense_data)
        category_field = form.fields['category_expense']

        # Проверка, что доступные категории содержат правильные варианты
        self.assertIn(('food', 'Продукты'), category_field.choices)
        self.assertIn(('car', 'Автомобиль'), category_field.choices)

        self.assertFalse(form.is_valid())  # Убедимся, что форма валидна при корректных данных

    def test_invalid_transaction_type(self):
        """Тестирование некорректного типа транзакции"""
        invalid_type_data = self.valid_data.copy()
        invalid_type_data['transaction_type'] = 'invalid_type'  # Некорректный тип транзакции

        form = TransactionForm(data=invalid_type_data)
        self.assertFalse(form.is_valid())  # Ожидаем, что форма не пройдет валидацию

