import uuid
from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nom de l'entreprise")
    address = models.TextField(blank=True, null=True, verbose_name="Adresse")
    contact_email = models.EmailField(blank=True, null=True, verbose_name="Email de contact")
    contact_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone de contact")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Entreprise"
        verbose_name_plural = "Entreprises"


class Location(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nom du lieu")
    address = models.TextField(blank=True, null=True, verbose_name="Adresse")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="locations", verbose_name="Entreprise")
    is_warehouse = models.BooleanField(default=False, verbose_name="Est un entrepôt")
    is_store = models.BooleanField(default=False, verbose_name="Est une boutique")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    def __str__(self):
        return f"{self.name} ({self.company.name})"

    class Meta:
        verbose_name = "Lieu"
        verbose_name_plural = "Lieux"


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom de catégorie")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, verbose_name="Nom du produit")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    sku = models.CharField(max_length=50, unique=True, verbose_name="Code SKU")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products", verbose_name="Catégorie")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    minimum_stock = models.IntegerField(default=10, verbose_name="Stock minimum")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date de mise à jour")

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def get_stock_in_location(self, location):
        """Retourne le stock actuel dans un lieu spécifique"""
        stock = StockLevel.objects.filter(product=self, location=location).first()
        return stock.current_quantity if stock else 0

    def is_stock_low(self, location=None):
        """Vérifie si le stock est bas pour ce produit, globalement ou dans un lieu spécifique"""
        if location:
            stock = self.get_stock_in_location(location)
            return stock < self.minimum_stock
        else:
            total_stock = sum(level.current_quantity for level in self.stock_levels.all())
            return total_stock < self.minimum_stock

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"



class StockLevel(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_levels", verbose_name="Produit")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="stock_levels", verbose_name="Lieu")
    initial_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Quantité initiale")
    current_quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Quantité actuelle")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    class Meta:
        unique_together = ('product', 'location')
        verbose_name = "Niveau de stock"
        verbose_name_plural = "Niveaux de stock"

    def __str__(self):
        return f"{self.product.name} à {self.location.name}: {self.current_quantity}"


class MovementType(models.Model):
    name = models.CharField(max_length=50, verbose_name="Type de mouvement")
    is_incoming = models.BooleanField(default=True, verbose_name="Est une entrée")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Type de mouvement"
        verbose_name_plural = "Types de mouvement"


class Movement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movements", verbose_name="Produit")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="movements", verbose_name="Lieu")
    movement_type = models.ForeignKey(MovementType, on_delete=models.PROTECT, verbose_name="Type de mouvement")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantité")
    reference_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Numéro de référence")
    comments = models.TextField(blank=True, null=True, verbose_name="Commentaires")
    performed_by = models.CharField(max_length=100, blank=True, null=True, verbose_name="Effectué par")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date du mouvement")

    def __str__(self):
        movement_direction = "entrée" if self.movement_type.is_incoming else "sortie"
        return f"{self.product.name}: {movement_direction} de {self.quantity} à {self.location.name}"

    def save(self, *args, **kwargs):

        stock, created = StockLevel.objects.get_or_create(
            product=self.product,
            location=self.location,
            defaults={'initial_quantity': 0, 'current_quantity': 0}
        )

        if self.movement_type.is_incoming:
            stock.current_quantity += self.quantity
        else:
            stock.current_quantity -= self.quantity

        stock.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"


class StockAlert(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
    ]

    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('acknowledged', 'Reconnu'),
        ('resolved', 'Résolu'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="alerts", verbose_name="Produit")
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="alerts", verbose_name="Lieu")
    current_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantité actuelle")
    minimum_quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantité minimum")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium', verbose_name="Priorité")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending', verbose_name="Statut")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="Date de résolution")

    def __str__(self):
        return f"Alerte: {self.product.name} à {self.location.name} ({self.current_quantity})"

    class Meta:
        verbose_name = "Alerte de stock"
        verbose_name_plural = "Alertes de stock"