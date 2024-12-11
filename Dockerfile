# Используем официальный образ Python
FROM python:3.9

# Установка зависимостей
RUN pip install --upgrade pip

# Копируем файл зависимостей
COPY requirements.txt /finance_manager_app/requirements.txt
RUN pip install -r /finance_manager_app/requirements.txt

# Копируем исходный код
COPY . /app
WORKDIR /app

# Устанавливаем переменные окружения
ENV DJANGO_ENV=production
ENV PYTHONUNBUFFERED=1

# Открываем порт
EXPOSE 8000

# Выполнение миграций и запуск приложения через gunicorn
CMD ["sh", "-c", "python manage.py migrate && gunicorn finance_manager_app.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
