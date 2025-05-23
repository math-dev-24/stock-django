from django.contrib.auth.models import User
from django.db import models, transaction
from catalog.models import Product
from django.db.models import F
from order.models import Company, Order


class Inventory(models.Model):
    id = models.AutoField(primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="inventory", verbose_name="Company")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventory", verbose_name="Product")
    in_stock = models.IntegerField(verbose_name="Quantity")
    in_transit = models.IntegerField(verbose_name="In transit")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    class Meta:
        unique_together = ('company', 'product')
        indexes = [
            models.Index(fields=['company', 'product']),
        ]

    def __str__(self):
        return f"{self.company.name} - {self.product.name} - {self.in_stock}"

    @classmethod
    @transaction.atomic
    def update_inventory(cls, company, product, quantity, from_or_to, state):
        inventory = Inventory.objects.filter(company=company, product=product)

        in_stock = 0
        in_transit = 0

        if from_or_to == "from":
            in_stock = -quantity
        elif from_or_to == "to" and state.group_state == "Finished":
            in_stock = quantity
            in_transit = -quantity
        elif from_or_to == "to" and state.group_state != "Finished":
            in_transit = quantity

        if not inventory.exists():
            cls.objects.create(
                company=company,
                product=product,
                in_stock=in_stock,
                in_transit=in_transit,
            )
        else:
            inventory.update(
                in_stock=F('in_stock') + in_stock,
                in_transit=F('in_transit') + in_transit
            )

    @classmethod
    def available_quantity(cls, company_id, product, needed_quantity) -> bool:
        inventory = Inventory.objects.filter(company_id=company_id, product=product)
        if not inventory.exists():
            return False
        return inventory.first().in_stock >= needed_quantity


class Log(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="logs", verbose_name="User")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="logs", verbose_name="Order", null=True)
    description = models.TextField(verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")