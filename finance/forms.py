from django import forms
from .models import Transaction




class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "category",
            "amount",
            "description",
            "date",
            "is_income"
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }