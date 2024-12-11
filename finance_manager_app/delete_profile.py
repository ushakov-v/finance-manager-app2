from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

@login_required
def delete_profile(request):
    """Удалить профиль пользователя"""
    user = request.user
    user.delete()  # Удаляем пользователя из базы данных
    return redirect('home')  # Перенаправляем на главную страницу (или другую страницу)
