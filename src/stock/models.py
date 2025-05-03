from django.contrib.auth.models import User
from django.db import models
from catalog.models import Product
from order.models import Company

from src.order.models import Order


class Inventory(models.Model):
    id = models.Index(models.AutoField(primary_key=True))
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="inventory", verbose_name="Company")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventory", verbose_name="Product")
    in_stock = models.IntegerField(verbose_name="Quantity")
    in_transit = models.IntegerField(verbose_name="In transit")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    def __str__(self):
        return f"{self.company.name} - {self.product.name} - {self.in_stock}"


class Log(models.Model):
    id = models.Index(models.AutoField(primary_key=True))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="logs", verbose_name="User")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="logs", verbose_name="Order", null=True)
    description = models.TextField(verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
