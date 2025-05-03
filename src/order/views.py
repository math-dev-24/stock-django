from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Company
from .forms import AddCompanyFrom


@login_required
def company_list_view(request):
    company = Company.objects.all()

    context = {
        'company': company,
        'nombre_company': company.count(),
    }

    return render(request, "order/companies/list.html", context)


@login_required
def add_company_view(request):
    if request.method == 'POST':
        form = AddCompanyFrom(request.POST)
        if form.is_valid():
            company = form.save()
            company.members.add(request.user)
            messages.success(request, "La société a été ajoutée avec succès.")
            return redirect('stock:company_detail', company.id)
        else:
            messages.error(request, "Une erreur est survenue.")
            return render(request, "order/companies/add.html", context={"form": form})

    form = AddCompanyFrom()
    return render(request, "order/companies/add.html", context={"form": form})


@login_required
def company_detail_view(request, id):
    try:
        company = Company.objects.get(pk=id)
        return render(request, "order/companies/detail.html", {
            "company": company
        })
    except Company.DoesNotExist:
        messages.error(request, "Cette société n'existe pas.")
        return redirect('stock:dashboard')


@login_required
def change_company(request):
    id_company = request.POST.get('company_id')
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')

    if not next_url:
        next_url = reverse('stock:dashboard')

    if not id_company:
        messages.error(request, "Veuillez sélectionner une société.")
        return redirect(next_url)

    try:
        company = Company.objects.get(pk=id_company)
        request.session['company_id'] = str(company.id)
        request.session['company_name'] = company.name
        request.session.modified = True
        messages.success(request, f"Magasin changé : {company.name}")
    except Company.DoesNotExist:
        messages.error(request, "Ce magasin n'existe pas.")

    return redirect(next_url)
