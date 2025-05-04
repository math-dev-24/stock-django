from . import views
from django.urls import path

app_name = 'stock'


urlpatterns = [
    path("", views.home_view, name="home"),
    path("dashboard", views.dashboard_view, name="dashboard"),
    path("flux", views.flux_view, name="flux"),
    path("inventory", views.inventory_view, name="inventory"),
]
