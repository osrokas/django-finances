from django_filters.views import FilterView
from django_tables2.tables import Table
from django_tables2.views import SingleTableView

from .models import Spending


class SpendingTable(Table):
    class Meta:
        model = Spending
        template_name = "django_tables2/semantic.html"
        fields = ["category", "description", "amount", "date"]


class FilteredSingleTableView(FilterView, SingleTableView):
    def get_table_data(self):
        data = super(FilteredSingleTableView, self).get_table_data()
        return data if self.object_list is None else self.object_list
