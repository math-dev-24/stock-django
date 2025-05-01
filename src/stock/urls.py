from . import views
from django.urls import path

app_name = 'stock'


urlpatterns = [
    path("", views.index, name="home"),

    path("dashboard", views.dashboard_view, name="dashboard"),

    path("add-product", views.add_product_view, name="addProduct"),
    path("add-category", views.add_category_view, name="addCategory"),
    path("add-company", views.add_company_view, name="addCompany"),

    path("companies/<uuid:id>", views.company_view, name="companies"),
    path("product/<uuid:id>", views.product_view, name="product"),

    path("product/<uuid:id>/delete", views.deleteProduct, name="productDelete"),
]