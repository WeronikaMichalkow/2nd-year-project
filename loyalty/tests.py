from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Loyalty

class LoyaltyTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def test_view_loyalty(self):
        response = self.client.get(reverse('view_loyalty'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Loyalty Points')

    def test_create_loyalty_for_user(self):
        self.assertEqual(Loyalty.objects.count(), 1)
        user2 = get_user_model().objects.create_user(
            username='testuser2', password='password123')
        self.client.login(username='testuser2', password='password123')
        response = self.client.get(reverse('view_loyalty'))
        self.assertEqual(Loyalty.objects.count(), 2)
        self.assertEqual(response.status_code, 200)
