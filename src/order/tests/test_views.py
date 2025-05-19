from django.test import TestCase
from django.urls import reverse


class OrderViewsTestCase(TestCase):
    fixtures = [
        'fixtures/states.json', 'fixtures/orders.json', 'fixtures/companies.json',
        'fixtures/products.json', 'fixtures/categories.json'
    ]

    def setUp(self):
        from django.contrib.auth.models import User
        User.objects.create_user(username='test', password='test')

    def test_list_company_view_with_permission(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse('order:company_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order/companies/list.html")
        self.assertEqual(response.context["nombre_company"], 5)

    def test_list_company_view_without_permission(self):
        response = self.client.get(reverse('order:company_list'))
        self.assertEqual(response.status_code, 302)

    def test_add_company_view_with_permission(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse('order:company_add'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order/companies/add.html")

    def test_add_company_view_without_permission(self):
        response = self.client.get(reverse('order:company_add'))
        self.assertEqual(response.status_code, 302)

    def test_state_list_view_with_permission(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse('order:state_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["count"], 5)

    def test_company_detail_view_with_permission(self):
        self.client.login(username="test", password="test")
        pk_company = "e86b1b4c-0e34-4ffc-9043-a5e621c4d6c3";
        name: str = "Digital Agency SARL"
        email: str = "info@digitalagency.fr"
        response = self.client.get(reverse('order:company_detail', kwargs={'id': pk_company}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order/companies/detail.html")

        context = response.context["company"]
        self.assertEqual(context.name, name)
        self.assertEqual(context.email, email)

    def test_company_list_view_without_permission(self):
        response = self.client.get(reverse('order:company_list'))
        self.assertEqual(response.status_code, 302)

    def test_state_list_view_without_permission(self):
        response = self.client.get(reverse('order:state_list'))
        self.assertEqual(response.status_code, 302)

    def test_order_detail_view_with_permission(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse('order:order_detail', kwargs={'order_id': "123e4567-e89b-12d3-a456-426614174000"}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "order/detail.html")

        context = response.context["order"]
        self.assertEqual(context.reference, "123456789")
        self.assertEqual(context.lines.count(), 1)

    def test_order_detail_view_without_permission(self):
        response = self.client.get(reverse('order:order_detail', kwargs={'order_id': "123e4567-e89b-12d3-a456-426614174000"}))
        self.assertEqual(response.status_code, 302)


