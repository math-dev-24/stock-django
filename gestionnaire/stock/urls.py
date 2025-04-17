from . import views
from django.urls import path

app_name = 'stock'


urlpatterns = [
    path("", views.index, name="home"),
    path("/login", views.login_view, name="login"),
    path("/logout", views.logout_view, name="logout"),
    path("/register", views.register_view, name="register"),
    path("/dashboard", views.dashboard_view, name="dashboard"),
    path("/account", views.account_view, name="account"),

    path("/add-product", views.add_product_view, name="addProduct")
]