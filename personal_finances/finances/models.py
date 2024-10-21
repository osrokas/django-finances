import pandas as pd
from django.db import models
from django.db.models import Sum


class Category(models.Model):
    """Category model"""
    category_name = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.category_name


class Spending(models.Model):
    """Spendings model"""
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.description
    
    @classmethod
    def totals_by_month(cls):
        select_data = {"month": """strftime('%%Y/%%m', date)"""}
        data = Spending.objects.extra(select=select_data).values('month').annotate(Sum("amount")).order_by()
        data = data.values('month', 'amount__sum')
        data = [row for row in data]

        return data
    
    @classmethod
    def spendings_by_date_range(cls, start_date, end_date):
        spendings = Spending.objects.filter(date__range=[start_date, end_date])

        if spendings:
            total_spendings = spendings.aggregate(total=Sum('amount'))
            total = total_spendings["total"]
            total = ("%.2f" % total)
        else:
            total = 0.00

        return total
    
    @classmethod
    def spendings_by_category_and_date_range(cls, start_date, end_date):
        spendings = Spending.objects.filter(date__range=[start_date, end_date])

        if spendings:
            data_category = []
            for category_spending in spendings:
                category_spending = {'category': category_spending.category.category_name, 'amount': category_spending.amount}
                data_category.append(category_spending)

            df_category = pd.DataFrame(data_category)
            df_category = df_category.groupby('category').sum()
            df_category = df_category.reset_index()

            labels_category = df_category['category'].tolist()
            values_category = df_category['amount'].tolist()

            return labels_category, values_category
        
        else:
            return [], []


class Income(models.Model):
    """Incomes model"""
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.description
    
    @classmethod
    def income_totals_by_month(cls):
        select_data = {"month": """strftime('%%Y/%%m', date)"""}
        data = Income.objects.extra(select=select_data).values('month').annotate(Sum("amount")).order_by()
        data = data.values('month', 'amount__sum')
        data = [row for row in data]

        return data
    
    @classmethod
    def income_by_date_range(cls, start_date, end_date):
        incomes = Income.objects.filter(date__range=[start_date, end_date])

        if incomes:
            total_incomes = incomes.aggregate(total=Sum('amount'))
            total_income = total_incomes["total"]
            total_income = "%.2f" % total_income
        else:
            total_income = 0.00

        return total_income

    @classmethod
    def income_by_category_and_date_range(cls, start_date, end_date):
        incomes = Income.objects.filter(date__range=[start_date, end_date])

        if incomes:
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
            
            return income_labels, income_values
            
        else:
            return [], []