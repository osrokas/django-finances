from django.contrib import admin

# Register your models here.
from .models import Spending, Category

admin.site.register([Spending, Category])
