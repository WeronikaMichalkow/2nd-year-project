from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from .models import Loyalty


class LoyaltyTestCase(TestCase):
    
    def test_view_loyalty_create_new_record(self):
        user = get_user_model().objects.create_user(username='testuser', password='password')
        client = self.client
        client.login(username='testuser', password='password')

        assert not Loyalty.objects.filter(user=user).exists()

        response = client.get(reverse('view_loyalty'))

        assert Loyalty.objects.filter(user=user).exists()
        assert response.status_code == 200
        assert 'loyalty' in response.context

    def test_view_loyalty_existing_record(self):
        user = get_user_model().objects.create_user(username='testuser', password='password')
        loyalty = Loyalty.objects.create(user=user)
        client = self.client
        client.login(username='testuser', password='password')

        response = client.get(reverse('view_loyalty'))

        assert response.status_code == 200
        assert 'loyalty' in response.context
        assert response.context['loyalty'] == loyalty

    def test_create_loyalty_for_user_new_record(self):
        user = get_user_model().objects.create_user(username='testuser', password='password')

        assert not Loyalty.objects.filter(user=user).exists()

        from .views import create_loyalty_for_user
        create_loyalty_for_user(user)

        assert Loyalty.objects.filter(user=user).exists()

    def test_create_loyalty_for_user_existing_record(self):
        user = get_user_model().objects.create_user(username='testuser', password='password')
        Loyalty.objects.create(user=user)

        assert Loyalty.objects.filter(user=user).exists()

        from .views import create_loyalty_for_user
        create_loyalty_for_user(user)

        loyalty_count = Loyalty.objects.filter(user=user).count()
        assert loyalty_count == 1
