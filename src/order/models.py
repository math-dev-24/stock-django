from django.contrib.auth.models import User
from django.db import models, transaction
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

    def __str__(self):
        return self.name + " - " + self.group_state


class LineOrder(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, related_name="orders", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", related_name="lines", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    comment = models.TextField(verbose_name="Commentaire")
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

    @classmethod
    @transaction.atomic
    def create_order_with_line(cls, reference, from_company_id, to_company_id, vat, state, line_orders):
        from stock.models import Inventory

        # Création de l'ordre
        tmp_order = Order.objects.create(
            reference=reference,
            vat=vat,
            state=state
        )
        # Setter les companies
        if from_company_id:
            tmp_order.from_company = Company.objects.get(pk=from_company_id)
        if to_company_id:
            tmp_order.to_company = Company.objects.get(pk=to_company_id)

        tmp_order.save(update_fields=["from_company", "to_company", 'updated_at'])

        # Création des lignes et ajustement de l'inventaire
        for line_order in line_orders:
            tmp_product = line_order['product']
            tmp_quantity = line_order['quantity']

            LineOrder.objects.create(
                order=tmp_order,
                product=tmp_product,
                quantity=tmp_quantity
            )

            if tmp_order.from_company:
                Inventory.update_inventory(tmp_order.from_company, tmp_product, tmp_quantity, "from", tmp_order.state)
            if tmp_order.to_company:
                Inventory.update_inventory(tmp_order.to_company, tmp_product, tmp_quantity, "to", tmp_order.state)

        return tmp_order

    @classmethod
    @transaction.atomic
    def update_order_state(cls, order_id, new_state):
        from stock.models import Inventory

        tmp_order = cls.objects.get(id=order_id)

        if new_state.group_state == "Finished" and tmp_order.to_company:
            for line_order in tmp_order.lines.all():
                Inventory.update_inventory(
                    tmp_order.to_company,
                    line_order.product,
                    line_order.quantity,
                    "to",
                    new_state
                )

        tmp_order.state = new_state
        tmp_order.save(update_fields=['state', 'updated_at'])

        return tmp_order
