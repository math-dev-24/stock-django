from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Product

# Create your views here.
def index(request):
    context = {
        'is_admin': request.user.is_staff,
        'user_name': request.user.username if request.user.is_authenticated else None
    }

    return render(request, 'stock/index.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('stock:dashboard')
        else:
            return render(request, 'stock/login.html', {
                'error_message' : 'Nom d\'utilisateur ou mot de passe incorrect !'
            })

    return render(request, 'stock/login.html')


def dashboard_view(request):
    products = Product.objects.all()

    context = {
        "products": products,
        "count": len(products)
    }

    return render(request, "stock/dashboard.html", context)


def logout_view(request):
    logout(request)
    return redirect('stock:home')


def register_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'stock/register.html', {
                'error_message': 'Les mots de passe ne correspondent pas.'
            })

        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            return render(request, 'stock/register.html', {
                'error_message': 'Ce nom d\'utilisateur existe déjà.'
            })

        # Créer un nouvel utilisateur
        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        messages.success(request, f'Compte créé avec succès pour {username}!')
        return redirect('stock:home')

    return render(request, 'stock/register.html')

@login_required
def account_view(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'stock/account.html', context)



def add_product_view(request):

    return render(request, "stock/product/add.html")