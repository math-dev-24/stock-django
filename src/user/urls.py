from . import views
from django.urls import path

app_name = 'user'

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("profile", views.profile_view, name="profile"),
]