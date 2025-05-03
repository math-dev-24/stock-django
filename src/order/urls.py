from django.urls import path
from . import views


app_name = 'order'

urlpatterns = [
    path("company", views.company_list_view, name="company_list"),
    path("company/add", views.add_company_view, name="company_add"),
    path("company/<uuid:id>", views.company_detail_view, name="company_detail"),
    path("company/change", views.change_company, name="change_company"),

]
