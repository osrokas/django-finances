from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path(route="", view=views.index, name="index"),
    path("table/", login_required(views.SpendingsListView.as_view())),
    path(route="add/", view=views.add_spending, name="add"),
    path(route="income/", view=views.add_income, name="income"),
    path(route="register/", view=views.registration, name="register"),
    path(route="login/", view=views.login, name="login"),
    path(route="logout/", view=views.logout, name="logout"),
]
