from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from stock.models import Inventory
from .models import Company
from catalog.models import Product, Price
from .models import StateOrder, Order
from .forms import AddCompanyFrom, AddStateOrderForm
from django.db.models import OuterRef, Subquery, F


@login_required
def company_list_view(request):
    company = Company.objects.filter(members=request.user)

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
        company = Company.objects.get(pk=id, members=request.user)

        return render(request, "order/companies/detail.html", {
            "company": company
        })
    
    except Company.DoesNotExist:
        messages.error(request, "Cette société n'existe pas ou vous n'avez pas accès.")
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
        company = Company.objects.get(pk=id_company, members=request.user)
        request.session['company_id'] = str(company.id)
        request.session['company_name'] = company.name
        request.session.modified = True
        messages.success(request, f"Magasin changé : {company.name}")
    except Company.DoesNotExist:
        messages.error(request, "Ce magasin n'existe pas ou vous n'avez pas accès.")

    return redirect(next_url)


@login_required
def add_order_view(request):

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
        reference = request.POST.get('reference', '')
        from_company_id = request.POST.get('from_company', '')
        to_company_id = request.POST.get('to_company', '')
        vat = request.POST.get('vat')
        state_id = request.POST.get('state')

        state = StateOrder.objects.get(pk=state_id)

        product_ids = request.POST.getlist('products[]')
        quantities = request.POST.getlist('quantities[]')

        is_valid: bool = True

        line_orders = [{
            "product": Product.objects.get(pk=product_id),
            "quantity": int(quantities[i])
        } for i, product_id in enumerate(product_ids)]

        # Check if product is available
        if from_company_id:
            for line in line_orders:
                if not Inventory.available_quantity(
                        from_company_id,
                        line["product"],
                        line["quantity"]
                ):
                    tmp_inv = Inventory.objects.filter(company_id=from_company_id, product=line["product"])
                    if tmp_inv:
                        messages.error(
                            request,
                            f"Produit : {line['product'].name}, Quantité : {line['quantity']}, Disponible : {tmp_inv.first().in_stock}"
                        )
                    else:
                        messages.error(request, "Produit non disponible.")
                    is_valid = False
                    break

        if not reference:
            messages.error(request, "Veuillez saisir une référence.")
            is_valid = False

        if not from_company_id and not to_company_id:
            messages.error(request, "Veuillez sélectionner au moins un magasin.")
            is_valid = False

        if not vat:
            messages.error(request, "Veuillez sélectionner une TVA.")
            is_valid = False
        
        if not check_order_access(request, from_company_id) or not check_order_access(request, to_company_id):
            messages.error(request, "Vous n'avez pas accès à l'entreprise source ou destination.")
            is_valid = False

        if not is_valid:
            return render(request, "order/add.html", context)

        try:
            order = Order.create_order_with_line(reference, from_company_id, to_company_id, vat, state, line_orders)
            messages.success(request, "L'ordre a été créé avec succès.")
            return redirect('order:order_detail', order.id)
        except Exception as e:
            messages.error(request, f"Une erreur est survenue : {e}")
            return render(request, "order/add.html", context)

    return render(request, "order/add.html", context)


@login_required
def add_state_view(request):
    if request.method == 'POST':
        form = AddStateOrderForm(request.POST)
        if form.is_valid():
            state = form.save()
            state.save()
            messages.success(request, "L'état a été ajouté avec succès.")
            return redirect('order:state_list')
        else:
            messages.error(request, "Une erreur est survenue.")
            return render(request, "order/state/add.html", context={"form": form})

    form = AddStateOrderForm()
    return render(request, "order/state/add.html", context={"form": form})


@login_required
def state_list_view(request):
    states = StateOrder.objects.all().order_by('group_state')
    context = {
        "states": states,
        "count": states.count()
    }
    return render(request, "order/state/list.html", context)


@login_required
def state_edit_view(request, state_id):
    try:
        state = StateOrder.objects.get(pk=state_id)
    except StateOrder.DoesNotExist:
        messages.error(request, "Cet état n'existe pas ou vous n'avez pas accès.")
        return redirect('order:state_list')

    if request.method == 'POST':
        form = AddStateOrderForm(request.POST, instance=state)
        if form.is_valid():
            state = form.save()
            messages.success(request, f"L'état \"{state.name}\" a été modifié avec succès.")
            return redirect('order:state_list')
        else:
            messages.error(request, "Une erreur est survenue.")
            return render(request, "order/state/edit.html", context={"form": form, "state": state})

    form = AddStateOrderForm(instance=state)
    return render(request, "order/state/edit.html", context={"form": form, "state": state})


@login_required
def company_edit_view(request, id):
    try:
        company = Company.objects.get(pk=id, members=request.user)
    except Company.DoesNotExist:
        messages.error(request, "Cette société n'existe pas ou vous n'avez pas accès.")
        return redirect('stock:dashboard')

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


@login_required
def order_detail_view(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)

        if not check_order_access(request, order):
            messages.error(request, "Vous n'avez pas accès à cette commande.")
            return redirect('stock:dashboard')

    except Order.DoesNotExist:
        messages.error(request, "Cette commande n'existe pas.")
        return redirect('stock:dashboard')
    
    context = {
        "order": order,
        "states": StateOrder.objects.all(),
    }
    
    return render(request, "order/detail.html", context)


@login_required
def order_edit_state_view(request, order_id):
    if not request.method == 'POST':
        return redirect('order:order_detail', order_id)

    state_id = request.POST.get('state')
    new_state = StateOrder.objects.get(pk=state_id)

    if not new_state:
        messages.error(request, "Veuillez sélectionner un état.")
        return redirect('order:order_detail', order_id)

    try:
        order = Order.update_order_state(order_id, new_state)
        messages.success(request, f"L'état a été modifié avec succès ({order.reference}).")
        return redirect('order:order_detail', order_id)
    except Exception as e:
        messages.error(request, f"Une erreur est survenue : {e}")
        return redirect('order:order_detail', order_id)


@login_required
def state_delete_view(request, state_id):
    if request.method == 'POST':
        try:
            state = StateOrder.objects.get(pk=state_id)
        except StateOrder.DoesNotExist:
            messages.error(request, "Cet état n'existe pas ou vous n'avez pas accès.")
            return redirect('order:state_list')

        orders_count = Order.objects.filter(state=state).count()

        if not check_state_access(request, state):
            messages.error(request, "Vous n'avez pas accès à cet état.")
            return redirect('order:state_list')

        if orders_count == 0:
            state.delete()
            messages.success(request, f"L'état \"{state.name}\" a été supprimé avec succès.")
            return redirect('order:state_list')
        else:
            messages.error(request, f"L'état \"{state.name}\" ne peut pas être supprimé car il y a des commandes associées.")
            return redirect('order:state_list')


def check_order_access(request, order):
    user_companies = Company.objects.filter(members=request.user)
    has_access = False

    if order.from_company and order.from_company in user_companies:
        has_access = True
    elif order.to_company and order.to_company in user_companies:
        has_access = True

    return has_access


def check_state_access(request, state):
    state_companies = StateOrder.objects.all()
    has_access = False

    if state.company and state.company in state_companies:
        has_access = True

    return has_access