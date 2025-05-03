from django.urls import path
from . import views


app_name = 'catalog'

urlpatterns = [

    # Product
    path("product", views.product_list_view, name="product_list"),
    path("product/<uuid:id>", views.product_view, name="product_detail"),
    path("product/add", views.add_product_view, name="product_add"),
    path("product/<uuid:id>/delete", views.delete_product, name="product_delete"),
    path("product/<uuid:id>/edit", views.edit_product, name="product_edit"),

    # Category
    path("category", views.category_list_view, name="category_list"),
    path("category/<int:id>", views.category_view, name="category_detail"),
    path("category/add", views.add_category_view, name="category_add"),
    path("category/<int:id>/delete", views.delete_category, name="category_delete"),
    path("category/<int:id>/edit", views.edit_category, name="category_edit"),

    # Price
    path("price/add/<uuid:product_id>", views.add_price_to_product, name="price_add"),
]
