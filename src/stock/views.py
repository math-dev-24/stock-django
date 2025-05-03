from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from catalog.models import Product, Category


def home_view(request):
    return render(request, 'stock/index.html')


@login_required
def dashboard_view(request):

    user_companies = request.user.company_members.all()
    products = Product.objects.all()
    categories = Category.objects.all()

    categories_json = []

    for category in categories:
        categories_json.append({
            'id': category.id,
            'name': category.name,
            'quantity': products.filter(category=category).count()
        })

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
        },
        "categories_json": categories_json
    }
    return render(request, "stock/dashboard.html", context)
