from django.db import models
import uuid


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name="Nom du produit")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")

    def __str__(self):
        return self.name

    @classmethod
    def create_category(cls, name, description):
        category = cls(name=name, description=description)
        category.save()
        return category


class Product(models.Model):
    class Unit(models.TextChoices):
        LITER = "liter", "Litre"
        WEIGHT = "weight", "Poids"
        PIECE = "piece", "Pièce"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, verbose_name="Nom du produit")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    sku = models.CharField(max_length=50, unique=True, verbose_name="Code SKU")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    category = models.ManyToManyField(Category, related_name="products", verbose_name="Catégories")
    unit = models.CharField(max_length=50, choices=Unit.choices, verbose_name="Unit", default=Unit.PIECE)

    def __str__(self):
        return self.name

    @classmethod
    def create_product(cls, name, sku, price, description=None, categories=None):
        product = cls(
            name=name,
            description=description,
            sku=sku
        )
        product.save()

        if categories:
            product.category.add(*categories)

        Price(product=product, price=price).save()
        return product

    @classmethod
    def get_product(cls, id):
        product = cls.objects.get(id=id)
        return product


class Price(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="prices", verbose_name="Produit")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")

    def __str__(self):
        return f"{self.product.name}: {self.price}"
