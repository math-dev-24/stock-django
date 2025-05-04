from django.urls import path
from . import views


app_name = 'order'

urlpatterns = [
    path("company", views.company_list_view, name="company_list"),
    path("company/add", views.add_company_view, name="company_add"),
    path("company/<uuid:id>", views.company_detail_view, name="company_detail"),
    path("company/<uuid:id>/edit", views.company_edit_view, name="company_edit"),
    path("company/change", views.change_company, name="change_company"),
    path("add", views.add_order_view, name="add_order"),


    # States
    path("state", views.state_list_view, name="state_list"),
    path("state/add", views.add_state_view, name="add_state"),
    path("state/<int:state_id>/edit", views.state_edit_view, name="state_edit"),

    #orders
    path("<uuid:order_id>/detail", views.order_detail_view, name="order_detail"),

    path("<uuid:order_id>/edit-state", views.order_edit_state_view, name="order_edit_state"),

]
