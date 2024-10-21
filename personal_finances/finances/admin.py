from django.contrib import admin

from .models import Spending, Category, Income


admin.site.register([Spending, Category, Income])
