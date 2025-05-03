from order.models import Company


def global_context_order(request):
    return {
        'nombre_company': Company.objects.count(),
        'company': Company.objects.all()
    }