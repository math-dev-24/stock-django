from django import forms
from .models import Product, Category


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

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('price') is None:
            raise forms.ValidationError("Veuillez remplir le nouveau prix.")
        return cleaned_data


class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'sku', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'sku': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'category': forms.SelectMultiple(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'})
        }

    def clean_sku(self):
        sku = self.cleaned_data['sku']
        if Product.objects.filter(sku=sku).count() > 1:
            raise forms.ValidationError("Le SKU existe déjà.")
        return sku

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-lg p-2 focus:border-indigo-500 focus:ring-indigo-500'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        if name is None:
            raise forms.ValidationError("Veuillez remplir le nom de la catégorie.")
        if Category.objects.filter(name=name).exists():
            raise forms.ValidationError("La catégorie existe déjà.")
        return cleaned_data
