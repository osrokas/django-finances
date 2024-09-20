from django.db import models


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


class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return self.description