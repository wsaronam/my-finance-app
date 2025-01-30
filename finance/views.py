from django.shortcuts import render, redirect
from django.db import models
from .models import Transaction
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm




def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # saves the user to db
            return redirect('login')  # redirects the user to the login screen
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    income = transactions.filter(is_income=True).aggregate(models.Sum('amount'))['amount__sum'] or 0
    expenses = transactions.filter(is_income=False).aggregate(models.Sum('amount'))['amount__sum'] or 0
    balance = income - expenses

    return render(request, 'dashboard.html', {
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
            print("Transaction saved!")  # for debugging
            return redirect('dashboard')
        else:
            print("Form is not valid:", form.errors)  # for debugging
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})


def home(request):
    return render(request, 'home.html')