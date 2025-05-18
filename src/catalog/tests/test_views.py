from django.test import TestCase
from django.urls import reverse


class ProductTest(TestCase):
    fixtures = ["fixtures/categories.json", "fixtures/products.json", "fixtures/prices.json"]

    def test_get_all_categories(self):
        response = self.client.get(reverse("catalog:category_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/category/list.html")
        self.assertEqual(response.context["count"], 25)