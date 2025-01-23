from django.shortcuts import render, redirect
from django.db import models
from .models import Transaction
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required




@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    income = transactions.filter(is_income=True).aggregate(models.Sum('amount'))['amount__sum'] or 0
    expenses = transactions.filter(is_income=False).aggregate(models.Sum('amount'))['amount__sum'] or 0
    balance = income - expenses

    return render(request, 'tracker/dashboard.html', {
        'transactions': transactions,
        'income': income,
        'expenses': expenses,
        'balance': balance,
    })


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'tracker/add_transaction.html', {'form': form})


def home(request):
    return render(request, 'home.html')