import django_tables2 as tables
from .models import Spending

class SpendingTable(tables.Table):
    class Meta:
        model = Spending
        template_name = "django_tables2/semantic.html"
        fields = ["category", "description", "amount", "date"]
