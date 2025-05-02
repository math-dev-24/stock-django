from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from order.models import Company


@login_required
def add_company_view(request):
    return render(request, "order/companies/add.html")


@login_required
def company_view(request, id):
    try:
        company = Company.objects.get(pk=id)

        return render(request, "order/companies/detail.html", {
            "company": company
        })
    except Company.DoesNotExist:
        messages.error(request, "Cette société n'existe pas.")
        return redirect('stock:dashboard')

