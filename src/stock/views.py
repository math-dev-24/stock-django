from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import AddProductForm
from .models import Product, Category, Company

from math import floor


def index(request):
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

    return render(request, 'stock/index.html', context)



@login_required
def dashboard_view(request):
    """
    Affiche le tableau de bord avec les produits, catégories et entreprises
    auxquelles l'utilisateur a accès.
    """
    user_companies = request.user.companies.all()
    products = Product.objects.all()
    categories = Category.objects.all()

    context = {
        "products": {
            "list": products,
            "count": products.count()
        },
        "categories": {
            "list": categories,
            "count": categories.count()
        },
        "companies": {
            "list": user_companies,
            "count": user_companies.count()
        }
    }

    return render(request, "stock/dashboard.html", context)


@login_required
def add_category_view(request):
    if request.method == 'POST':
        category_name = request.POST.get('name')
        category_description = request.POST.get('description')

        if category_name is None or category_description is None:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, "stock/category/add.html")
        else:
            category = Category.create_category(category_name, category_description)
            messages.success(request, f"La catégorie \"{category.name}\" a été ajoutée avec succès.")
            return redirect('stock:dashboard')

    return render(request, "stock/category/add.html")


@login_required
def add_product_view(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=True)

            messages.success(request, f"Le produit {product.name} a été ajouté avec succès.")
            return redirect('stock:dashboard')
        else:
            return render(request, "stock/product/add.html", context={"form": form})
    form = AddProductForm()
    return render(request, "stock/product/add.html", context={"form": form})


@login_required
def product_view(request, id):
    product = Product.objects.get(pk=id)

    if request.method == 'POST':
        price = request.POST.get('price')

        if price is None:
            messages.error(request, "Veuillez remplir le nouveau prix.")
            return render(request, "stock/product/detail.html", {
                "product": product
            })
        else:
            product.prices.create(price=price)
            messages.success(request, f"Le prix {price}€ a été ajouté avec succès.")
            return redirect('stock:product', id)

    return render(request, "stock/product/detail.html", {
        "product": product
    })


@login_required
def deleteProduct(request, id):
    product = Product.get_product(id)
    product.delete()
    messages.success(request, f"Le produit {product.name} a été supprimé avec succès.")
    return redirect('stock:home')


@login_required
def company_view(request, id):
    try:
        company = Company.objects.get(pk=id)

        return render(request, "stock/companies/detail.html", {
            "company": company
        })
    except Company.DoesNotExist:
        messages.error(request, "Cette société n'existe pas.")
        return redirect('stock:dashboard')


@login_required
def add_company_view(request):
    return render(request, "stock/companies/add.html")