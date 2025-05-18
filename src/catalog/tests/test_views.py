from django.test import TestCase
from django.urls import reverse

from catalog.models import Category
from django.contrib.auth.models import User


class ProductTest(TestCase):
    fixtures = ["fixtures/categories.json", "fixtures/products.json", "fixtures/prices.json"]

    def setUp(self):
        User.objects.create_user(username='test', password='test')

    def test_get_all_categories(self):
        response = self.client.get(reverse("catalog:category_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/category/list.html")
        self.assertEqual(response.context["count"], 25)

    def test_get_category(self):
        response = self.client.get(reverse("catalog:category_detail", args=[1]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/category/detail.html")
        self.assertEqual(response.context["category"].name, "Électronique")

    def test_delete_category_with_permission(self):
        self.client.login(username="test", password="test")

        response = self.client.post(reverse("catalog:category_delete", args=[1]))

        self.assertRedirects(response, reverse("catalog:category_list"))
        self.assertFalse(Category.objects.filter(id=1).exists())

    def test_delete_category_without_permission(self):
        response = self.client.post(reverse("catalog:category_delete", args=[1]))
        self.assertEqual(response.status_code, 302)