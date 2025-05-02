from django.urls import path
from . import views


app_name = 'catalog'

urlpatterns = [
    path("product", views.product_list_view, name="product_list"),
    path("product/<uuid:id>", views.product_view, name="product_detail"),
    path("product/add", views.add_product_view, name="product_add"),
    path("product/<uuid:id>/delete", views.delete_product, name="product_delete"),

    path("category/add", views.add_category_view, name="category_add"),
]
