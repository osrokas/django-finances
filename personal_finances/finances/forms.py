from django import forms
from .models import Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserLoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter your username"}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"placeholder": "Enter your password"}))

    class Meta:
        model = User
        fields = ['username', 'password']

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Enter a username"}))
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Enter your first name"}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Enter your last name"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class SpendingsForm(forms.Form):
    category = forms.ModelChoiceField(
        label="Category",
        queryset=Category.objects.all(),
        to_field_name="category_name",
        required=False,
        widget=forms.Select(
            attrs={
                "class": "category-select",
                "name": "category",
                "placeholder": "Select a category",
                "required": "True",
            }
        ),
    )
    amount = forms.DecimalField(
        label="Amount",
        required=False,
        widget=forms.NumberInput(attrs={"step": "0.01", "required": "True", "placeholder": "Enter an amount"}),
    )
    date = forms.DateField(
        label="Date",
        required=False,
        widget=forms.TextInput(attrs={"type": "date", "required": "True", "placeholder": "Select a date"}),
    )
    description = forms.CharField(label="Description", required=False, max_length=500, widget=forms.Textarea(attrs={"required": "False", "placeholder": "Write a description"}))


class IncomeForm(forms.Form):
    amount = forms.DecimalField(
        label="Amount",
        required=False,
        widget=forms.NumberInput(
            attrs={"step": "0.01", "placeholder": "Enter an amount", "required": "True"}
        ),
    )
    date = forms.DateField(
        label="Date",
        required=False,
        widget=forms.TextInput(
            attrs={"type": "date", "required": "True", "placeholder": "Select a date"}
        ),
    )
    description = forms.CharField(
        label="Description",
        required=False,
        max_length=500,
        widget=forms.Textarea(
            attrs={"required": "False", "placeholder": "Write a description"}
        ),
    )
