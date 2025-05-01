from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

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


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username is None or password is None:
            return render(request, 'stock/login.html', {
                'error_message': 'Veuillez remplir tous les champs.'
            })

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bonjour {user.username}, vous êtes maintenant connecté.')
            return redirect('stock:dashboard')
        else:
            return render(request, 'stock/login.html', {
                'error_message': 'Email ou mot de passe incorrect !'
            })

    return render(request, 'stock/login.html')


def logout_view(request):
    logout(request)
    return redirect('stock:home')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if username is None or email is None or password1 is None or password2 is None:
            return render(request, 'stock/login.html', {
                'error_message': 'Veuillez remplir les champs.'
            })

        if password1 != password2:
            return render(request, 'stock/register.html', {
                'error_message': 'Les mots de passe ne correspondent pas.'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'stock/register.html', {
                'error_message': 'Ce nom d\'utilisateur existe déjà.'
            })

        user = User.objects.create_user(username=username, email=email, password=password1)

        login(request, user)

        messages.success(request, f'Compte créé avec succès pour {username}! Vous êtes maintenant connecté.')
        return redirect('stock:home')

    return render(request, 'stock/register.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import Product, Category, Company


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
def account_view(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'stock/account.html', context)


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
    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        sku = request.POST.get('sku')
        category = request.POST.getlist('category')

        if name is None or description is None or price is None or sku is None or category is None:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, "stock/product/add.html", {
                "categories": categories
            })
        else:
            product = Product.create_product(name, sku, price, description, category)
            messages.success(request, f"Le produit {product.name} a été ajouté avec succès.")
            return redirect('stock:dashboard')

    return render(request, "stock/product/add.html", {
        "categories": categories,
    })


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