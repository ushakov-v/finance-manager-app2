# app/views.py
from django.shortcuts import render, get_object_or_404
from .models import Transaction

def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'app/transaction_list.html', {'transactions': transactions})

def transaction_detail(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    return render(request, 'app/transaction_detail.html', {'transaction': transaction})
