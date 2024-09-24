from math import log
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django_tables2 import SingleTableView
from .models import Category, Spending, Income
from .tables import SpendingTable
import pandas as pd
from .forms import SpendingsForm, IncomeForm, UserRegisterForm, UserLoginForm
from django.db.models import Sum
from .utils import current_month_range
from django.contrib.auth import authenticate, login as login_user, logout as logout_user


@login_required
def index(request):

    start_date, end_date = current_month_range()
    # filter and sum all spendings for the current month
    spendings = Spending.objects.filter(date__range=[start_date, end_date])
    total_spendings = spendings.aggregate(total=Sum('amount'))
    total = total_spendings["total"]

    total = ("%.2f" % total)

    data = []

    for spending in spendings:
        spending = {
            "category": spending.category.category_name,
            "amount": spending.amount,
        }
        data.append(spending)

    df = pd.DataFrame(data)
    df = df.groupby("category").sum()
    df = df.reset_index()

    labels = df["category"].tolist()
    values = df["amount"].tolist()

    # Income
    incomes = Income.objects.filter(date__range=[start_date, end_date])
    total_incomes = incomes.aggregate(total=Sum('amount'))
    total_income = total_incomes["total"]
    total_income = "%.2f" % total_income

    balance = float(total_income) - float(total)

    data_income = []
    for income in incomes:
        _income = {
            "category": income.description,
            "amount": income.amount,
        }
        data_income.append(_income)

    df = pd.DataFrame(data_income)

    income_labels = df["category"].tolist()
    income_values = df["amount"].tolist()

    context = {
        "balance": balance,
        "total": total,
        "labels": labels,
        "values": values,
        "total_income": total_income,
        "income_labels": income_labels,
        "income_values": income_values
    }
    return render(request, "spendings/index.html", context)


def detail(request, spending_id):
    return HttpResponse(f"Spending on {spending_id}")


class SpendingsListView(SingleTableView):
    model = Spending
    table_class = SpendingTable
    template_name = "spendings/spending.html"

@login_required
def chart_response(request):
    start_date, end_date = current_month_range()

    spendings = Spending.objects.filter(date__range=[start_date, end_date])

    data = []

    for spending in spendings:
        spending = {'category': spending.category.category_name, 'amount': spending.amount}
        data.append(spending)

    df = pd.DataFrame(data)
    df = df.groupby('category').sum()
    df = df.reset_index()

    labels = df['category'].tolist()
    values = df['amount'].tolist()

    context = {
        "labels": labels,
        "values": values,
    }
    return render(request, "spendings/chart.html", context)

@login_required
def add_spending(request):
    form = SpendingsForm(request.POST)
    if request.method == "POST":
        print(request)
        if form.is_valid():

            amount = request.POST.get("amount")
            date = request.POST.get("date")
            category = request.POST.get("category")
            category_id = Category.objects.get(category_name=category).id
            description = request.POST.get("description")
            spending = Spending(
                amount=amount,
                date=date,
                category=Category(int(category_id)),
                description=description,
            )
            spending.save()
            text = {'text': 'Spending added successfully'}
            return render(request, "spendings/add.html", {"form": form, "text": text})
    else:
        return render(request, "spendings/add.html", {"form": form})

@login_required
def add_income(request):
    form = IncomeForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            amount = request.POST.get("amount")
            date = request.POST.get("date")
            description = request.POST.get("description")
            income = Income(amount=amount, date=date, description=description)
            income.save()
            text = {'text': 'Income added successfully'}
            return render(request, "spendings/income.html", {"form": form, "text": text})
    else:
        return render(request, "spendings/income.html", {"form": form})


def login(request, message=None):
    form = UserLoginForm(request.POST)

    if request.method == "POST":
        try:
            if form.is_valid():
                username = request.POST.get("username")
                password = request.POST.get("password")

                user = authenticate(request, username=username, password=password)
                login_user(request=request, user=user)
                if user is not None:
                    return redirect(index)
                else:
                    return redirect(login)
        except Exception as e:
            login_error = {"error": "Invalid username or password"}
            context = {"form": form, "login_error": login_error}
            return redirect(login)

    elif request.method == "GET":
        return render(request, "spendings/login.html", {"form": form})


def registration(request):

    form = UserRegisterForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            print(form.is_valid())
            form.save()
            return redirect(login)
        elif form.errors:
            return redirect(registration)
        else:
            return redirect(registration)
    else:
        return render(request, "spendings/register.html", {"form": form})

def logout(request):
    logout_user(request)
    return redirect("login")
