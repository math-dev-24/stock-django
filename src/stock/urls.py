from . import views
from django.urls import path

app_name = 'stock'


urlpatterns = [
    path("", views.home_view, name="home"),
    path("dashboard", views.dashboard_view, name="dashboard")
]
