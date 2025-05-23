from django import forms
from .models import Company, StateOrder


class AddCompanyFrom(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'email', 'phone', 'address', 'city', 'zipcode', 'is_store', 'is_warehouse']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'phone': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'address': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'city': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'zipcode': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'is_store': forms.CheckboxInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'is_warehouse': forms.CheckboxInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
        }


class AddStateOrderForm(forms.ModelForm):
    class Meta:
        model = StateOrder
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'group_state': forms.Select(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
        }