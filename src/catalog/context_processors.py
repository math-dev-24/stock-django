from catalog.models import Product, Category


def global_context(request):
    return {
        'nombre_produits': Product.objects.count(),
        'nombre_categories': Category.objects.count()
    }