from django.urls import path
from . import views


app_name = 'order'

urlpatterns = [
    path("company/add", views.add_company_view, name="company_add"),
    path("company/<uuid:id>", views.company_view, name="company_detail"),
]
