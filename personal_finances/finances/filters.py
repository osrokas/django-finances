from django_filters.widgets import DateRangeWidget
import django_filters
from .models import Spending, Category

class TableFilters(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(
        widget=DateRangeWidget(attrs={"type": "date", "placeholder": "yyyy-mm-dd"})
    )
    description = django_filters.CharFilter(lookup_expr="icontains", label="Description")
    category = django_filters.ModelChoiceFilter(lookup_expr="exact", queryset=Category.objects.all())
    amount = django_filters.RangeFilter(field_name="amount")

    class Meta:
        class Meta:
            model = Spending
            fields = ["description", "date", "category", "amount"]
