from django import forms
from .models import Category


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
