from django.contrib.auth.models import User
from django.db import models
import uuid
from catalog.models import Product


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, verbose_name="Nom de la société")
    email = models.EmailField(verbose_name="E-mail")
    phone = models.CharField(max_length=15, verbose_name="Téléphone")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    members = models.ManyToManyField(User, related_name="company_members", verbose_name="members")
    address = models.CharField(max_length=150, verbose_name="Adresse", default="12 rue de la Paix")
    city = models.CharField(max_length=150, verbose_name="City", default="Paris")
    zipcode = models.CharField(max_length=15, verbose_name="Zipcode", default="75001")
    is_store = models.BooleanField(default=False, verbose_name="Is store")
    is_warehouse = models.BooleanField(default=False, verbose_name="Is warehouse")

    def __str__(self):
        return self.name


class StateOrder(models.Model):
    class Group(models.TextChoices):
        OPEN = "Open", "Open"
        PENDING = "Pending", "Pending"
        BLOCKED = "Blocked", "Blocked"
        FINISHED = "Finished", "Finished"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name="Nom", default="Open")
    group_state = models.CharField(max_length=20, choices=Group.choices, default=Group.OPEN)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")


class Order(models.Model):
    class VAT(models.TextChoices):
        REDUCED = "5.5", "Réduit 5.5%"
        INTERMEDIATE = "10", "Intermédiaire 10%"
        NORMAL = "20", "Normal 20%"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=150, verbose_name="Référence")
    # Si null, c'est une arrivée de stock
    from_company = models.ForeignKey(Company, related_name="order_from", on_delete=models.CASCADE, null=True)
    # Si null, c'est une vente, au voir faire au pire plus tard un statut customer
    to_company = models.ForeignKey(Company, related_name="order_to", on_delete=models.CASCADE, null=True)
    state = models.ForeignKey(StateOrder, related_name="state_order", on_delete=models.CASCADE)
    vat = models.CharField(max_length=20, choices=VAT.choices, default=VAT.NORMAL)
    ttc = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Toutes taxes comprises", null=True)
    ht = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Hors Taxe", null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")


class LineOrder(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, related_name="orders", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="lines", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    comment = models.TextField(verbose_name="Commentaire")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")


