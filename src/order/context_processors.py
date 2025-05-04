from .models import Company, Order, StateOrder


def global_context_order(request):
    current_company = request.current_company

    return {
        'nombre_company': Company.objects.count(),
        'company': Company.objects.all(),
        "nombre_state": StateOrder.objects.count(),
        "nombre_order": Order.objects.filter(to_company=current_company).count() +
                        Order.objects.filter(from_company=current_company).count()
    }
