from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from catalog.models import Product, Category
from order.models import Order, Company
from .models import Inventory


def home_view(request):
    return render(request, 'stock/index.html')


@login_required
def dashboard_view(request):

    user_companies = request.user.company_members.all()
    products = Product.objects.all()
    categories = Category.objects.all()

    categories_json_list = []

    for category in categories:
        categories_json_list.append({
            "id": category.id,
            "name": category.name,
            "quantity": products.filter(category=category).count()
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
        "categories_json_list": categories_json_list
    }
    return render(request, "stock/dashboard.html", context)


@login_required
def flux_view(request):
    current_company = request.current_company

    command_in = Order.objects.filter(to_company=current_company)
    command_out = Order.objects.filter(from_company=current_company)

    context = {
        "command_in": {
            "list": command_in,
            "count": command_in.count()
        },
        "command_out": {
            "list": command_out,
            "count": command_out.count()
        }
    }
    return render(request, "stock/flux.html", context)


@login_required
def inventory_view(request):
    current_company = request.current_company

    inventories = Inventory.objects.filter(company=current_company)

    context = {
        "inventories": {
            "list": inventories,
            "count": inventories.count()
        },
        "count": inventories.count()
    }
    return render(request, "stock/inventory.html", context)


@login_required
def inventory_detail_view(request, inventory_id):
    current_company = request.current_company
    inventory = Inventory.objects.get(pk=inventory_id)

    command_in = Order.objects.filter(
        to_company=current_company,
        lines__product=inventory.product
    ).distinct()

    command_out = Order.objects.filter(
        from_company=current_company,
        lines__product=inventory.product
    ).distinct()

    context = {
        "inventory": inventory,
        "command_in": command_in,
        "command_out": command_out
    }

    return render(request, "stock/inventory-detail.html", context)


@login_required
def inventory_export_view(request):
    import csv
    from django.http import HttpResponse

    user = request.user

    companies = Company.objects.filter(members=user)

    inventories = Inventory.objects.filter(company__in=companies)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

    writer = csv.writer(response)
    writer.writerow(["id", "company", "product", "in_stock", "in_transit", "updated_at"])

    # Données
    for inventory in inventories:
        writer.writerow([
            inventory.id,
            inventory.company.name,
            inventory.product.name,
            inventory.in_stock,
            inventory.in_transit,
            inventory.updated_at
        ])

    return response
