from django import forms
from .models import Product


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'price': forms.NumberInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'sku': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'category': forms.SelectMultiple(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'})
        }

