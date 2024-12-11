"""
URL configuration for finance_manager_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, transactions_view, add_transaction, edit_transaction, delete_transaction, \
    transaction_list, profile_view, delete_profile
from .views import get_balance
from .views import register_view, login_view, logout_view

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    path('', transaction_list, name='transaction_list'),
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('api/', include(router.urls)),
    path('api/balance/', get_balance, name='get_balance'),
    path('register/', register_view, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('transactions/', transaction_list, name='transaction_list'),
    path('add/', add_transaction, name='add_transaction'),
    path('edit/<int:pk>/', edit_transaction, name='edit_transaction'),
    path('delete/<int:pk>/', delete_transaction, name='delete_transaction'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('test/', lambda request: HttpResponse('Test Page'), name='test_page')

]

def api_form(request):
    return render(request, 'api_form.html')

urlpatterns += [
    path('api-form/', api_form, name='api_form'),
]
