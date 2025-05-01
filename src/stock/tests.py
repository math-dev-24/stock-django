from django.test import TestCase
from decimal import Decimal
from .models import User, Category, Product, Price


class ModelsTestCase(TestCase):
    def setUp(self):
        # Création de données de base pour les tests
        self.user = User.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )

        self.category1 = Category.create_category(
            name="Électronique",
            description="Produits électroniques"
        )

        self.category2 = Category.create_category(
            name="Smartphones",
            description="Téléphones mobiles"
        )

    def test_user_creation(self):
        """Test de la création d'un utilisateur"""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

        # Vérifier que le mot de passe est bien haché
        self.assertNotEqual(self.user.password, "password123")

    def test_category_creation(self):
        """Test de la création d'une catégorie"""
        self.assertEqual(self.category1.name, "Électronique")
        self.assertEqual(self.category1.description, "Produits électroniques")

        # Vérifier la représentation en chaîne
        self.assertEqual(str(self.category1), "Électronique")

    def test_product_creation(self):
        """Test de la création d'un produit avec des catégories et un prix"""
        product = Product.create_product(
            name="iPhone 14",
            sku="IP14-001",
            description="Le dernier iPhone d'Apple",
            price=Decimal("999.99"),
            categories=[self.category1, self.category2]
        )

        # Vérifier les informations du produit
        self.assertEqual(product.name, "iPhone 14")
        self.assertEqual(product.sku, "IP14-001")
        self.assertEqual(product.description, "Le dernier iPhone d'Apple")

        # Vérifier que les catégories ont été ajoutées
        self.assertEqual(product.category.count(), 2)
        self.assertIn(self.category1, product.category.all())
        self.assertIn(self.category2, product.category.all())

        # Vérifier que le prix a été créé
        self.assertEqual(product.prices.count(), 1)
        self.assertEqual(product.prices.first().price, Decimal("999.99"))

        # Vérifier la représentation en chaîne
        self.assertEqual(str(product), "iPhone 14")

    def test_price_creation(self):
        """Test de la création d'un prix pour un produit existant"""
        product = Product.create_product(
            name="Samsung Galaxy",
            sku="SG-001",
            description="Un smartphone Samsung",
            price=Decimal("899.99")
        )

        # Vérifier le prix initial
        self.assertEqual(product.prices.count(), 1)
        initial_price = product.prices.first()
        self.assertEqual(initial_price.price, Decimal("899.99"))

        # Créer un nouveau prix (pour simuler un changement de prix)
        new_price = Price(product=product, price=Decimal("849.99"))
        new_price.save()

        # Vérifier que le produit a maintenant deux prix
        product.refresh_from_db()  # Recharger depuis la base de données
        self.assertEqual(product.prices.count(), 2)

        # Vérifier que le nouveau prix est bien enregistré
        prices = list(product.prices.order_by('-created_at'))
        self.assertEqual(prices[0].price, Decimal("849.99"))
        self.assertEqual(prices[1].price, Decimal("899.99"))