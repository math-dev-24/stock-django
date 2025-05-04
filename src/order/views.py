from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Company
from catalog.models import Product, Price
from .models import StateOrder
from .forms import AddCompanyFrom, AddStateOrderForm
from django.db.models import OuterRef, Subquery, F


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


@login_required
def add_order_view(request):
    products = Product.objects.all()
    states = StateOrder.objects.all()

    latest_prices = Price.objects.filter(
        product=OuterRef('pk')
    ).order_by('-created_at').values('price')[:1]

    products = Product.objects.all().annotate(
        latest_price=Subquery(latest_prices)
    )

    states = StateOrder.objects.all()
    products_json_list = list(products.values('id', 'name', latest_price=F('latest_price')))

    context = {
        "products": products,
        "states": states,
        "products_json_list": products_json_list
    }

    if request.method == 'POST':
        # TODO : faire validation du formulaire
        print(f"TODO : {request.POST}")
        reference = request.POST.get('reference', '')
        from_company_id = request.POST.get('from_company', '')
        to_company_id = request.POST.get('to_company', '')
        vat = request.POST.get('vat')
        state = request.POST.get('state')

        product_ids = request.POST.getlist('products[]')
        quantities = request.POST.getlist('quantities[]')

        is_valid = True

        # Check
        if not reference:
            messages.error(request, "Veuillez saisir une référence.")
            is_valid = False
        if not from_company_id and not to_company_id:
            messages.error(request, "Veuillez sélectionner au moins un magasin.")
            is_valid = False
        if not vat:
            messages.error(request, "Veuillez sélectionner une TVA.")
            is_valid = False

        if not is_valid:
            return render(request, "order/add.html", context)

        print(f"TODO : créer l'ordre")

    return render(request, "order/add.html", context)


@login_required
def add_state_view(request):
    if request.method == 'POST':
        form = AddStateOrderForm(request.POST)
        if form.is_valid():
            state = form.save()
            state.save()
            messages.success(request, "L'état a été ajouté avec succès.")
            return redirect('stock:state_list')
        else:
            messages.error(request, "Une erreur est survenue.")
            return render(request, "order/state/add.html", context={"form": form})

    form = AddStateOrderForm()
    return render(request, "order/state/add.html", context={"form": form})


@login_required
def state_list_view(request):
    states = StateOrder.objects.all()
    context = {
        "states": states,
        "count": states.count()
    }
    return render(request, "order/state/list.html", context)


@login_required
def state_edit_view(request, id):
    state = StateOrder.objects.get(pk=id)
    if request.method == 'POST':
        form = AddStateOrderForm(request.POST, instance=state)
        if form.is_valid():
            state = form.save()
            messages.success(request, "L'état a été modifié avec succès.")
            return redirect('order:state_list')
        else:
            messages.error(request, "Une erreur est survenue.")
            return render(request, "order/state/edit.html", context={"form": form, "state": state})

    form = AddStateOrderForm(instance=state)
    return render(request, "order/state/edit.html", context={"form": form, "state": state})


@login_required
def company_edit_view(request, id):
    company = Company.objects.get(pk=id)
    if request.method == 'POST':
        form = AddCompanyFrom(request.POST, instance=company)
        if form.is_valid():
            company = form.save()
            messages.success(request, "La société a été modifiée avec succès.")
            return redirect('order:company_detail', company.id)
        else:
            messages.error(request, "Une erreur est survenue.")
            return render(request, "order/companies/edit.html", context={"form": form, "company": company})

    form = AddCompanyFrom(instance=company)
    return render(request, "order/companies/edit.html", context={"form": form, "company": company})


