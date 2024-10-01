import django_tables2 as tables
from .models import Spending
from django_tables2.views import SingleTableView
from django_filters.views import FilterView

class SpendingTable(tables.Table):
    class Meta:
        model = Spending
        template_name = "django_tables2/semantic.html"
        fields = ["category", "description", "amount", "date"]


class FilteredSingleTableView(FilterView, SingleTableView):

    def get_table_data(self):
        data = super(FilteredSingleTableView, self).get_table_data()
        return data if self.object_list is None else self.object_list
