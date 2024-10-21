import django_filters
from django.forms import widgets
from django_filters.widgets import DateRangeWidget, RangeWidget

from .models import Spending, Category


class TableFilters(django_filters.FilterSet):
    # Make date a date range filter on the same line
    date = django_filters.DateFromToRangeFilter(
        widget=DateRangeWidget(attrs={"type": "date", "placeholder": "yyyy-mm-dd", "style": "display: inline;"})
    )
    description = django_filters.CharFilter(lookup_expr="icontains", label="Description", widget=widgets.TextInput(attrs={"style": "display: inline;" }))
    category = django_filters.ModelChoiceFilter(lookup_expr="exact", queryset=Category.objects.all(), widget=widgets.Select(attrs={"style": "display: inline;"}))
    amount = django_filters.RangeFilter(field_name="amount", widget=RangeWidget(attrs={"style": "display: inline;"}))

    class Meta:
        class Meta:
            model = Spending
            fields = ["description", "date", "category", "amount"]
