from django.test import TestCase

from catalog.models import Product, Category


class ProductTest(TestCase):
    fixtures = ["fixtures/categories.json", "fixtures/products.json", "fixtures/prices.json"]

    def test_products_count(self):
        self.assertEqual(Product.objects.count(), 40)

    def test_categories_count(self):
        self.assertEqual(Category.objects.count(), 25)

    def test_category(self):
        category = Category.objects.get(name="Électronique")
        self.assertEqual(category.name, "Électronique")
        self.assertEqual(category.description, "Tous les produits électroniques, gadgets et appareils")
        self.assertEqual(category.products.count(), 12)
