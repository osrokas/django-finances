from math import e
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as login_user, logout as logout_user

from .models import Category, Spending, Income
from .tables import FilteredSingleTableView, SpendingTable
from .filters import TableFilters
from .utils import current_month_range, total_month_data_parser
from .forms import (
    SpendingsForm,
    IncomeForm,
    UserRegisterForm,
    UserLoginForm,
)


@login_required
def index(request):
    """Index view"""
    # Get the start and end date of the current month
    start_date, end_date = current_month_range()

    # Filter and sum all spendings for the current month
    monthly_spendings_total = Spending.spendings_by_date_range(start_date, end_date)

    # Filter and sum all incomes for the current month
    monthly_income_total = Income.income_by_date_range(start_date, end_date)

    # Filter and sum all spendings for the current month by category
    spent_labels, spent_values = Spending.spendings_by_category_and_date_range(start_date, end_date)

    # Filter and sum all incomes for the current month by category
    income_labels, income_values = Income.income_by_category_and_date_range(start_date, end_date)

    # Get totals by month
    totals_by_month = Spending.totals_by_month()
    total_by_month_amounts, total_by_month_labels = total_month_data_parser(totals_by_month)

    # Get totals by month for incomes
    income_totals_by_month = Income.income_totals_by_month()
    income_by_month_amounts, income_by_month_labels = total_month_data_parser(income_totals_by_month)

    # Total spendings by category form all time
    total_spendings_by_category_labels, total_spendings_by_category_amounts = Spending.spendings_by_category_and_date_range("1900-01-01", end_date)

    # Calculate the balance
    monthly_balance = float(monthly_income_total) - float(monthly_spendings_total)
    monthly_balance = round(monthly_balance, 2)

    # Get spent by day
    spent_by_day_labels, spent_by_day_values = Spending.spent_by_day(start_date, end_date)

    # Income by day
    income_by_day_labels, income_by_day_values = Income.income_by_day(start_date, end_date)

    # Total spendings
    total_spendings = Spending.spendings_by_date_range("1900-01-01", end_date)

    # Total incomes
    total_incomes = Income.income_by_date_range("1900-01-01", end_date)

    # Totals balance
    total_balance = float(total_incomes) - float(total_spendings) + 34.55 # Amount of the start balance without cash
    total_balance = round(total_balance, 2)

    last_spendings_data = Spending.last_spendings()

    # Context for the template
    context = {
        "balance": monthly_balance,
        "total": monthly_spendings_total,
        "spent_labels": spent_labels,
        "spent_values": spent_values,
        "total_income": monthly_income_total,
        "total_by_month_amounts": total_by_month_amounts,
        "total_by_month_labels": total_by_month_labels,
        "income_by_month_amounts": income_by_month_amounts,
        "income_by_month_labels": income_by_month_labels,
        "income_labels": income_labels,
        "income_values": income_values,
        "category_labels": total_spendings_by_category_labels,
        "category_values": total_spendings_by_category_amounts,
        "spent_by_day_labels": spent_by_day_labels,
        "spent_by_day_values": spent_by_day_values,
        "income_by_day_labels": income_by_day_labels,
        "income_by_day_values": income_by_day_values,
        "total_spendings": total_spendings,
        "total_incomes": total_incomes,
        "total_balance": total_balance,
        "last_spendings_data": last_spendings_data,
    }

    # Render the template
    return render(request, "spendings/index.html", context)


class SpendingsListView(FilteredSingleTableView):
    """Table view for spendings"""
    model = Spending
    table_class = SpendingTable
    template_name = "spendings/spending.html"
    filterset_class = TableFilters
    paginate_by = 20


@login_required
def add_spending(request):
    """Add spending view"""
    # Get the form
    form = SpendingsForm(request.POST)

    # Check if the form is valid
    if request.method == "POST":

        if form.is_valid():
            # Get the form data
            amount = request.POST.get("amount")
            date = request.POST.get("date")
            category = request.POST.get("category")
            category_id = Category.objects.get(category_name=category).id
            description = request.POST.get("description")

            # Create the spending
            spending = Spending(
                amount=amount,
                date=date,
                category=Category(int(category_id)),
                description=description,
            )

            # Save the spending to the database
            spending.save()

            # Message for the user
            text = {'text': 'Spending added successfully'}

            # Clean the form
            form = SpendingsForm()

            # Render the template
            return render(request, "spendings/add.html", {"form": form, "text": text})
        
    else:
        # Render the template
        return render(request, "spendings/add.html", {"form": form})


@login_required
def add_income(request):
    """Add income view"""
    # Get the form
    form = IncomeForm(request.POST)

    # Check if the form is valid
    if request.method == "POST":
        # Check if the form is valid
        if form.is_valid():
            # Get the form data
            amount = request.POST.get("amount")
            date = request.POST.get("date")
            description = request.POST.get("description")
            # Create Income
            income = Income(amount=amount, date=date, description=description)
            # Save the income to the database
            income.save()
            # Message for the user
            text = {'text': 'Income added successfully'}
            # Clean the form
            form = IncomeForm()
            # Render the template
            return render(request, "spendings/income.html", {"form": form, "text": text})
    else:
        # Render the template
        return render(request, "spendings/income.html", {"form": form})


def login(request, message=None):
    """Login view"""
    # Get the form
    form = UserLoginForm(request.POST)

    # Check if the form is valid
    if request.method == "POST":
        try:
            # Check if the form is valid
            if form.is_valid():
                # Get the form data
                username = request.POST.get("username")
                password = request.POST.get("password")
                # Authenticate the user
                user = authenticate(request, username=username, password=password)
                # Login the user
                login_user(request=request, user=user)
                # Check if the user is authenticated
                if user is not None:
                    # Redirect to the index
                    return redirect(index)
                else:
                    # Redirect to the login if the user is not authenticated
                    return redirect(login)
        except Exception as e:
            # Login error
            login_error = {"error": "Invalid username or password"}
            # Render the template
            context = {"form": form, "login_error": login_error}
            return redirect(login)

    elif request.method == "GET":
        # Render the template
        return render(request, "spendings/login.html", {"form": form})


def registration(request):
    """Registration view"""
    # Get the form
    form = UserRegisterForm(request.POST)

    # Check if the form is valid
    if request.method == "POST":
        # Check if the form is valid
        if form.is_valid():
            # Save the form
            form.save()
            # Redirect to the login
            return redirect(login)
        
        # If the form is not valid redirect to the registration
        elif form.errors:
            # Redirect to the registration
            return redirect(registration)
        else:
            # Redirect to the registration
            return redirect(registration)
    else:
        # Render registration template if the method is GET
        return render(request, "spendings/register.html", {"form": form})


def logout(request):
    """Logout view"""
    # Logout the user
    logout_user(request)
    # Redirect to the login
    return redirect("login")
