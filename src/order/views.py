from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Company
from catalog.models import Product, Price
from stock.models import Inventory
from .models import StateOrder, Order, LineOrder
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
        reference = request.POST.get('reference', '')
        from_company_id = request.POST.get('from_company', '')
        to_company_id = request.POST.get('to_company', '')
        vat = request.POST.get('vat')
        state_id = request.POST.get('state')

        product_ids = request.POST.getlist('products[]')
        quantities = request.POST.getlist('quantities[]')

        is_valid = True

        line_orders = [{
            "product": Product.objects.get(pk=product_id),
            "quantity": int(quantities[i])
        } for i, product_id in enumerate(product_ids)]

        if not reference:
            messages.error(request, "Veuillez saisir une référence.")
            is_valid = False
        if not from_company_id and not to_company_id:
            messages.error(request, "Veuillez sélectionner au moins un magasin.")
            is_valid = False

        if not vat:
            messages.error(request, "Veuillez sélectionner une TVA.")
            is_valid = False

        # je vérifie si les produits sont disponibles
        if from_company_id:
            from_company = Company.objects.get(pk=from_company_id)
            for line_order in line_orders:
                inventory_tmp = from_company.inventory.get(product=line_order['product'])
                if not inventory_tmp:
                    messages.error(request, f"Le produit {line_order['product'].name} n'existe pas.")
                    is_valid = False
                # Cas produit en stock inférieur à la quantité demandée
                if is_valid and inventory_tmp.in_stock < line_order['quantity']:
                    messages.error(request, f"Le produit {line_order['product'].name} n'est pas en stock (disponible: {inventory_tmp.in_stock}).")
                    is_valid = False

        if not is_valid:
            return render(request, "order/add.html", context)

        state = StateOrder.objects.get(pk=state_id)

        order = Order.objects.create(
            reference=reference,
            vat=vat,
            state=state
        )

        if from_company_id:
            order.from_company = Company.objects.get(pk=from_company_id)
        if to_company_id:
            order.to_company = Company.objects.get(pk=to_company_id)

        order.save()

        for line_order in line_orders:
            tmp_product = Product.objects.get(pk=line_order['product_id'])
            tmp_quantity = line_order['quantity']

            LineOrder.objects.create(
                order=order,
                product=tmp_product,
                quantity=tmp_quantity,
            )
            # update ou ajouter dans l'inventaire
            inventory_tmp = order.to_company.inventory.filter(product=tmp_product)
            in_stock = tmp_quantity
            in_transit = 0

            if state.group_state != "Terminated":
                in_transit = tmp_quantity
                in_stock = 0

            if not inventory_tmp.exists():
                Inventory.objects.create(
                    company=order.to_company,
                    product=tmp_product,
                    in_stock=in_stock,
                    in_transit=in_transit,
                )
            else:
                inventory_tmp.update(in_stock=F('in_stock') + in_stock, in_transit=F('in_transit') + in_transit)

        messages.success(request, "L'ordre a été créé avec succès.")
        return redirect('order:order_detail', order.id)

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
def state_edit_view(request, state_id):
    state = StateOrder.objects.get(pk=state_id)

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


@login_required
def order_detail_view(request, order_id):
    order = Order.objects.get(pk=order_id)
    states = StateOrder.objects.all()
    context = {
        "order": order,
        "states": states,
    }
    return render(request, "order/detail.html", context)


@login_required
def order_edit_state_view(request, order_id):
    if not request.method == 'POST':
        return redirect('order:order_detail', order_id)

    order = Order.objects.get(pk=order_id)
    state = request.POST.get('state')

    if not state:
        messages.error(request, "Veuillez sélectionner un état.")
        return redirect('order:order_detail', order_id)

    order.state = StateOrder.objects.get(pk=state)
    order.save()

    if order.state.group_state == "Finished":
        for line_order in order.lines.all():
            inventory_tmp = order.to_company.inventory.get(product=line_order.product)
            inventory_tmp.in_stock += line_order.quantity
            inventory_tmp.in_transit -= line_order.quantity
            inventory_tmp.save()

    messages.success(request, f"L'état a été modifié avec succès pour l'ordre {order.reference}.")
    return redirect('order:order_detail', order_id)
