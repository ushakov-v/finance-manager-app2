from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework.viewsets import ModelViewSet
from .forms import TransactionForm
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Transaction
from collections import defaultdict
import matplotlib.pyplot as plt
import io
import urllib, base64
from django import forms
from django.db import models



class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionForm
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type', 'date']

CATEGORY_TRANSLATIONS = {
    # Доходы
    'salary': 'Зарплата',
    'other': 'Другие источники',
    # Расходы
    'mandatory': 'Обязательные расходы',
    'food': 'Продукты',
    'car': 'Автомобиль',
    'entertainment': 'Развлечения',
    'household': 'Товары для дома',
    'selfcare': 'Забота о себе',
    'education': 'Образование',
    'miscellaneous': 'Разное',
}

@login_required
def transaction_list(request):
    # Получаем параметр фильтрации из запроса (по умолчанию 'all')
    filter_type = request.GET.get('type', 'all')

    # Фильтрация транзакций по типу (доходы или расходы)
    if filter_type == 'IN':
        transactions = Transaction.objects.filter(user=request.user, transaction_type='income').order_by('-date')
    elif filter_type == 'EX':
        transactions = Transaction.objects.filter(user=request.user, transaction_type='expense').order_by('-date')
    else:
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    # Подготовка данных для диаграммы по категориям
    categories_data = defaultdict(lambda: {'income': 0, 'expense': 0})
    for transaction in transactions:
        if transaction.transaction_type == 'income':
            categories_data[transaction.category_income]['income'] += transaction.amount
        elif transaction.transaction_type == 'expense':
            categories_data[transaction.category_expense]['expense'] += transaction.amount

    # Подготовка данных для диаграммы
    labels = []
    sizes = []

    for category, values in categories_data.items():
        translated_category = CATEGORY_TRANSLATIONS.get(category, category)  # Переводим категорию
        if values['income'] > 0:
            labels.append(f"{translated_category} (Доходы)")
            sizes.append(values['income'])
        if values['expense'] > 0:
            labels.append(f"{translated_category} (Расходы)")
            sizes.append(values['expense'])

    error_message = None
    img_url = None

    if not sizes:
        error_message = "Нет данных для генерации диаграммы."
    else:
        try:
            # Генерация круговой диаграммы
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  # Сделать круговой график

            img_buf = io.BytesIO()
            plt.savefig(img_buf, format='png')
            img_buf.seek(0)

            img_url = base64.b64encode(img_buf.getvalue()).decode('utf-8')

        except Exception as e:
            error_message = "Ошибка при генерации диаграммы."

    return render(request, 'transaction_list.html', {
        'transactions': transactions,
        'filter_type': filter_type,
        'img_url': img_url,
        'error_message': error_message,
    })


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Информация обновлена.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})

@api_view(['GET'])
def get_balance(request):
    """Get total balance (Income - Expense)."""
    income = Transaction.objects.filter(type='IN').aggregate(Sum('amount'))['amount__sum'] or 0
    expense = Transaction.objects.filter(type='EX').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = income - expense
    return Response({'income': income, 'expense': expense, 'balance': balance})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна.')
            return redirect('transaction_list')  # Перенаправление на страницу транзакций
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы вошли в систему.')
            return redirect('transaction_list')  # Перенаправление на страницу транзакций
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы.')
    return redirect('login')

@login_required
def transactions_view(request):
    # Предполагаем, что у вас есть модель Transaction
    from .models import Transaction  # Замените на путь к вашей модели
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    return render(request, 'app/../app/templates/transactions.html', {'transactions': transactions})

@login_required
def delete_profile(request):
    """Удалить профиль пользователя"""
    user = request.user
    user.delete()  # Удаляем пользователя из базы данных
    return redirect('login')  # Перенаправляем на главную страницу (или другую страницу)


# Добавление новой транзакции
@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user  # связываем транзакцию с текущим пользователем
            transaction.save()
            return redirect('transaction_list')  # или любой другой URL
    else:
        form = TransactionForm()

    return render(request, 'add_transaction.html', {'form': form})


# Редактирование транзакции
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'edit_transaction.html', {'form': form})


# Удаление транзакции
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')

    return render(request, 'delete_transaction.html', {'transaction': transaction})


# def transaction_list(request):
#     transactions = Transaction.objects.all()
#     return render(request, 'transaction_list.html', {'transactions': transactions})