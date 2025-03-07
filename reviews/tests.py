from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Review

User = get_user_model()

class ReviewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.review_data = {
            'review_text': 'This is a test review.',
            'rating': 5
        }

    def test_reviews_view_get(self):
        response = self.client.get(reverse('reviews:reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'reviews')

    def test_reviews_view_post_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('reviews:reviews'), self.review_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(user=self.user).exists())

    def test_reviews_view_post_unauthenticated(self):
        response = self.client.post(reverse('reviews:reviews'), self.review_data)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(user=self.user).exists())

    def test_review_model_str(self):
        review = Review.objects.create(user=self.user, review_text='Test review text', rating=4)
        self.assertEqual(str(review), 'Review by testuser - Rating: 4')

    def test_review_creation(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('reviews:reviews'), {
            'review_text': 'Amazing product!',
            'rating': 4
        })
        self.assertEqual(response.status_code, 302)
        review = Review.objects.last()
        self.assertEqual(review.review_text, 'Amazing product!')
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.user, self.user)
