from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('stock.urls')),
    path("order/", include('order.urls')),
    path("catalog/", include('catalog.urls')),
    path("auth/", include("user.urls"))
]
