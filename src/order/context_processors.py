from .models import Company, Order, StateOrder


def global_context_order(request):
    current_company = request.current_company

    if request.user.is_authenticated:
        user_companies = Company.objects.filter(members=request.user)
        number_company = user_companies.count()
    else:
        user_companies = Company.objects.none()
        number_company = 0

    return {
        'nombre_company': number_company,
        'company': user_companies,
        "nombre_state": StateOrder.objects.count(),
        "nombre_order": Order.objects.filter(to_company=current_company).count() +
                        Order.objects.filter(from_company=current_company).count()
    }
