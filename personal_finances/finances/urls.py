from django.urls import path

from . import views

urlpatterns = [
    path(route="", view=views.index, name="index"),
    path(route="chart/", view=views.chart_response, name="chart"),
    path("table/", views.SpendingsListView.as_view()),
    path(route="<int:spending_id>/", view=views.detail, name="detail"),
    path(route="add/", view=views.add_spending, name="add"),
    path(route="income/", view=views.add_income, name="income"),
]
