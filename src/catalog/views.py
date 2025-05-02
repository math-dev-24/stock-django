from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from catalog.forms import AddProductForm, AddCategoryForm
from catalog.models import Product
from math import floor


def product_list_view(request):
    products = Product.objects.all()
    params = request.GET.dict()

    items_per_page = 6
    page = int(params.get('page', 1))
    max_page = floor(len(products)/items_per_page)+1

    context = {
        'is_admin': request.user.is_staff,
        'user_name': request.user.username if request.user.is_authenticated else None,
        'products': products[items_per_page*(page-1):items_per_page*page],
        'count': len(products),
        "max_page": max_page,
        "page": page
    }

    return render(request, "catalog/product/list.html", context)


@login_required
def add_product_view(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=True)

            messages.success(request, f"Le produit {product.name} a été ajouté avec succès.")
            return redirect('stock:dashboard')
        else:
            return render(request, "catalog/product/add.html", context={"form": form})
    form = AddProductForm()
    return render(request, "catalog/product/add.html", context={"form": form})


@login_required
def product_view(request, id):
    product = Product.objects.get(pk=id)

    if request.method == 'POST':
        price = request.POST.get('price')

        if price is None:
            messages.error(request, "Veuillez remplir le nouveau prix.")
            return render(request, "catalog/product/detail.html", {
                "product": product
            })
        else:
            product.prices.create(price=price)
            messages.success(request, f"Le prix {price}€ a été ajouté avec succès.")
            return redirect('stock:product', id)

    return render(request, "catalog/product/detail.html", { "product": product })


@login_required
def delete_product(request, id):
    product = Product.get_product(id)
    product.delete()
    messages.success(request, f"Le produit {product.name} a été supprimé avec succès.")
    return redirect('catalog:product_list')


@login_required
def add_category_view(request):
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request, f"La catégorie {form.cleaned_data['name']} a été ajoutée avec succès.")
            return redirect('stock:dashboard')
        else:
            return render(request, "catalog/category/add.html", context={"form": form})

    form = AddCategoryForm()
    return render(request, "catalog/category/add.html", context={"form": form})
