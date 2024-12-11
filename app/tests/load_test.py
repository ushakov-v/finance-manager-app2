from locust import HttpUser, task, between
from random import randint
from time import sleep
import re


class FinanceManagerUser(HttpUser):
    wait_time = between(1, 50)

    def on_start(self):
        """Получаем CSRF токен и логинимся перед выполнением задач."""
        # Выполняем GET-запрос для получения CSRF токена
        response = self.client.get("/register/")
        csrf_token = self.extract_csrf_token(response.text)
        self.csrf_token = csrf_token

        # Выполняем регистрацию и логин (если необходимо)
        self.register_and_login()

    def extract_csrf_token(self, html):
        """Извлекаем CSRF токен из HTML."""
        match = re.search(r'name="csrfmiddlewaretoken" value="(.+?)"', html)
        return match.group(1) if match else None

    def get_headers(self):
        """Возвращаем заголовки с CSRF токеном для POST-запросов."""
        return {
            "X-CSRFToken": self.csrf_token,
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def register_and_login(self):
        """Регистрируем и логинимся."""
        # Генерация уникального имени для регистрации
        username = f"user{randint(1, 1000)}"
        password = "password123"
        email = f"{username}@example.com"

        # Регистрация пользователя
        registration_data = {
            'username': username,
            'password1': password,
            'password2': password,
            'email': email,
            'csrfmiddlewaretoken': self.csrf_token
        }
        self.client.post('/register/', registration_data, headers=self.get_headers())

        # Обновляем CSRF токен после регистрации
        response = self.client.get('/accounts/login/')
        self.csrf_token = self.extract_csrf_token(response.text)

        # Логин пользователя
        login_data = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': self.csrf_token
        }
        self.client.post('/accounts/login/', login_data, headers=self.get_headers())

        # Обновляем CSRF токен после логина
        self.csrf_token = self.extract_csrf_token(response.text)

    @task(1)
    def view_transactions(self):
        """Тестирование получения списка транзакций."""
        self.client.get('/transactions')
        sleep(2)

    @task(2)
    def add_transaction(self):
        """Тестирование добавления новой транзакции."""
        data = {
            'transaction_type': 'income',
            'amount': randint(10, 1000),  # случайная сумма
            'date': '2024-12-01',  # фиксированная дата для простоты
            'description': 'Test Transaction'
        }
        self.client.post('/add/', data, headers=self.get_headers())
        sleep(2)

    @task(3)
    def edit_transaction(self):
        """Тестирование редактирования транзакции."""
        transaction_id = randint(1, 100)  # Случайный ID транзакции
        data = {
            'transaction_type': 'expense',
            'amount': randint(10, 1000),
            'date': '2024-12-01',
            'description': 'Edited Test Transaction'
        }
        self.client.post(f'/edit/{transaction_id}/', data, headers=self.get_headers())
        sleep(2)

    @task(4)
    def delete_transaction(self):
        """Тестирование удаления транзакции."""
        transaction_id = randint(1, 100)  # Случайный ID транзакции
        # Отправляем запрос на удаление, как если бы пользователь сразу нажал "Да" в попапе
        self.client.post(f'/delete/{transaction_id}/', headers=self.get_headers())
        sleep(2)

    @task(5)
    def view_profile(self):
        """Тестирование доступа к профилю пользователя (требует логина)."""
        self.client.get('/profile/')
        sleep(2)

    @task(6)
    def logout(self):
        """Тестирование выхода из системы."""
        self.client.get('/logout/', headers=self.get_headers())
        sleep(2)


# Повторные задачи (повторные запросы с задержкой)
class RepeatedUser(FinanceManagerUser):
    wait_time = between(5, 10)  # Более длинная задержка между повторными запросами
