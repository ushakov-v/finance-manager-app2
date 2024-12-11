from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount', 'date', 'description', 'category_income', 'category_expense']

    # Поле для типа транзакции
    transaction_type = forms.ChoiceField(
        choices=Transaction.TRANSACTION_TYPES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Поле для суммы (с числовым вводом)
    amount = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Введите сумму'})
    )

    # Поле для даты
    date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )

    # Поле для описания
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите описание'})
    )

    # Категория для доходов (если тип транзакции - "Доход")
    category_income = forms.ChoiceField(
        choices=Transaction.CATEGORY_INCOME,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    # Категория для расходов (если тип транзакции - "Расход")
    category_expense = forms.ChoiceField(
        choices=Transaction.CATEGORY_EXPENSE,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Делаем поле категории необязательным для начальной загрузки
        self.fields['category_income'].required = False
        self.fields['category_expense'].required = False

        # Убираем поле категории по умолчанию (или заменяем на пустое поле)
        self.fields['category_income'].choices = [('', 'Выберите категорию')] + list(
            self.fields['category_income'].choices)
        self.fields['category_expense'].choices = [('', 'Выберите категорию')] + list(
            self.fields['category_expense'].choices)

        # Вызов метода для обновления категорий в зависимости от типа транзакции
        transaction_type = self.data.get('transaction_type', None)  # Получаем тип транзакции
        if transaction_type:
            self._set_category_choices(transaction_type)

    def _set_category_choices(self, transaction_type):
        """Обновление списка категорий в зависимости от типа транзакции"""
        if transaction_type == 'income':
            self.fields['category_expense'].choices = []  # Очищаем категории расходов, если доход
            self.fields['category_income'].choices = Transaction.CATEGORY_INCOME
        elif transaction_type == 'expense':
            self.fields['category_income'].choices = []  # Очищаем категории доходов, если расход
            self.fields['category_expense'].choices = Transaction.CATEGORY_EXPENSE
        else:
            self.fields['category_income'].choices = []
            self.fields['category_expense'].choices = []


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']