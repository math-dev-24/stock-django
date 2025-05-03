from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from catalog.models import Product, Category


def home_view(request):
    return render(request, 'stock/index.html')


@login_required
def dashboard_view(request):

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

