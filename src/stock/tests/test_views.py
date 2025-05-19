from django.test import TestCase
from django.urls import reverse


class StockViewsTestCase(TestCase):
    fixtures = [
        'fixtures/states.json', 'fixtures/orders.json', 'fixtures/companies.json',
        'fixtures/products.json', 'fixtures/categories.json'
    ]

    def setUp(self):
        from django.contrib.auth.models import User
        User.objects.create_user(username='test', password='test')

    def test_dashboard_view_with_permission(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse('stock:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stock/dashboard.html")
        self.assertEqual(response.context["companies"]["count"], 2)
        self.assertEqual(response.context["products"]["count"], 40)
        self.assertEqual(response.context["categories"]["count"], 25)

    def test_dashboard_view_without_permission(self):
        response = self.client.get(reverse('stock:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_flux_view_with_permission(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse('stock:flux'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stock/flux.html")
        self.assertEqual(response.context["command_out"]["count"], 0)
        self.assertEqual(response.context["command_in"]["count"], 2)

    def test_flux_view_without_permission(self):
        response = self.client.get(reverse('stock:flux'))
        self.assertEqual(response.status_code, 302)

    def test_inventory_view_with_permission(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse('stock:inventory'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stock/inventory.html")
        self.assertEqual(response.context["count"], 0)