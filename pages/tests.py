from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product

class PagesTests(TestCase):

    def setUp(self):
        self.men_category = Category.objects.create(name='Men', description='Men category')
        self.kids_category = Category.objects.create(name='kids', description='Kids category')
        self.women_category = Category.objects.create(name='women', description='Women category')

        Product.objects.create(name='Men Product 1', description='Men product description', price=10.00, category=self.men_category)
        Product.objects.create(name='Kids Product 1', description='Kids product description', price=15.00, category=self.kids_category)
        Product.objects.create(name='Women Product 1', description='Women product description', price=20.00, category=self.women_category)

    def test_homepage_view(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_mens_view(self):
        response = self.client.get(reverse('mens'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'mens.html')
        self.assertContains(response, 'Men Product 1')

    def test_kids_view(self):
        response = self.client.get(reverse('kids'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'kids.html')
        self.assertContains(response, 'Kids Product 1')

    def test_womens_view(self):
        response = self.client.get(reverse('womens'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'womens.html')
        self.assertContains(response, 'Women Product 1')

    def test_womens_view_empty_category(self):
        empty_category = Category.objects.create(name='Empty', description='No products')
        response = self.client.get(reverse('womens'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No products available')
