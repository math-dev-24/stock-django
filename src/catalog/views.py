from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from catalog.forms import AddProductForm, AddCategoryForm, EditProductForm
from catalog.models import Product, Category
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


def category_list_view(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
        "count": len(categories)
    }
    return render(request, "catalog/category/list.html", context)


def category_view(request, id):
    category = Category.objects.get(pk=id)
    context = {
        "category": category
    }
    return render(request, "catalog/category/detail.html", context)


@login_required
def delete_category(request, id):
    category = Category.objects.get(pk=id)
    category.delete()
    messages.success(request, f"La catégorie \"{category.name}\" a été supprimée avec succès.")
    return redirect('catalog:category_list')


@login_required
def add_price_to_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    price = request.POST.get('price')

    print(price)

    if price is None:
        messages.error(request, "Veuillez remplir le nouveau prix.")
        return render(request, "catalog/product/detail.html", {
            "product": product
        })
    else:
        product.prices.create(price=price)
        messages.success(request, f"Le prix {price}€ a été ajouté avec succès.")
        return redirect('catalog:product_detail', product_id)


@login_required
def edit_product(request, id):
    product = Product.objects.get(pk=id)

    if request.method == 'POST':
        form = EditProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Le produit \"{product.name}\" a été modifié avec succès.")
            return redirect('catalog:product_detail', id=id)
        else:
            return render(request, "catalog/product/edit.html", context={"form": form, "product": product})

    form = EditProductForm(instance=product)
    return render(request, "catalog/product/edit.html", context={"form": form, "product": product})


@login_required
def edit_category(request, id):
    category = Category.objects.get(pk=id)

    if request.method == 'POST':
        form = AddCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"La catégorie \"{category.name}\" a été modifiée avec succès.")
            return redirect('catalog:category_detail', id=id)
        else:
            return render(request, "catalog/category/edit.html", context={"form": form, "category": category})

    form = AddCategoryForm(instance=category)
    return render(request, "catalog/category/edit.html", context={"form": form, "category": category})