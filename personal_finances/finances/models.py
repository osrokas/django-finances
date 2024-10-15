from django.db import models
from django.db.models import Sum

class Category(models.Model):
    category_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.category_name

class Spending(models.Model):
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


class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.description