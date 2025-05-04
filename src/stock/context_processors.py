from .models import Inventory


def global_context_stock(request):
    return {
        'nombre_inventories': Inventory.objects.filter(company=request.current_company).count(),
    }