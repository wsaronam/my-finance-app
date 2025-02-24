from django.shortcuts import render, redirect
from django.db import models
from django.db.models import Sum
from .models import Transaction
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import json
from decimal import Decimal
from collections import defaultdict




# signup page ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # saves the user to db
            return redirect('login')  # redirects the user to the login screen
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


# login stuff ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
            print("Form is not valid:", form.errors)  # for debugging
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})


# home stuff ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def home(request):
    return render(request, 'home.html')


# dashboard stuff ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('date')
    income = transactions.filter(is_income=True).aggregate(models.Sum('amount'))['amount__sum'] or Decimal(0)
    expenses = transactions.filter(is_income=False).aggregate(models.Sum('amount'))['amount__sum'] or Decimal(0)
    balance = income - expenses

    # Group transactions by date
    transactionsDaily = defaultdict(Decimal)  # Dictionary to hold summed values per date
    for transaction in transactions:
        transactionsDaily[transaction.date.strftime("%Y-%m-%d")] += transaction.amount if transaction.is_income else -transaction.amount
    
    # for line graph
    dates = []
    balances = []
    runningBalance = Decimal(0)

    datesSorted = sorted(transactionsDaily.keys())
    for date in datesSorted:
        runningBalance += transactionsDaily[date]
        dates.append(date)
        balances.append(float(runningBalance))


    # get categories for pie chart
    category_expenses = (
        transactions.filter(is_income=False)
        .values("category")
        .annotate(total=Sum("amount"))
        .order_by("-total")
    )
    
    categories = [entry['category'] for entry in category_expenses]
    expenses = [float(entry['total']) for entry in category_expenses]
    expenseSum = sum(expenses)


    # get income vs expenses per month
    monthlyData = transactions.values('date__month', 'date__year').annotate(
        total_income=Sum('amount', filter=models.Q(is_income=True)),
        total_expense=Sum('amount', filter=models.Q(is_income=False))
    ).order_by('date__year', 'date__month')

    vsMonths = []
    vsIncomes = []
    vsExpenses = []
    for data in monthlyData:
        month_label = f"{data['date__year']}-{str(data['date__month']).zfill(2)}"
        vsMonths.append(month_label)
        vsIncomes.append(float(data['total_income'] or 0))
        vsExpenses.append(float(data['total_expense'] or 0))


    return render(request, 'dashboard.html', {
        'transactions': transactions,
        'income': round(income, 2),
        'expenses': expenses,
        'expenseSum': round(expenseSum, 2),
        'balance': round(balance, 2),
        'dates': json.dumps(dates),
        'balances': json.dumps(balances),
        'categories': json.dumps(categories),
        'expenses': json.dumps(expenses),
        'vsMonths': json.dumps(vsMonths),
        'vsIncomes': json.dumps(vsIncomes),
        'vsExpenses': json.dumps(vsExpenses),
    })


