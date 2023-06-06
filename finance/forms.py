from django import forms
from .models import BanqueTransactions, CaisseTransactions

class BanqueTransactionsForm(forms.ModelForm):
    class Meta:
        model = BanqueTransactions
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class CaisseTransactionsForm(forms.ModelForm):
    class Meta:
        model = CaisseTransactions
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
