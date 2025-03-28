from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Product, Size
from cart.models import Cart, CartItem
from loyalty.models import Loyalty
import stripe
from unittest.mock import patch


class CartViewTests(TestCase):

    def setUp(self):
        
        self.user = User.objects.create_user(username="testuser", password="password")
        self.product = Product.objects.create(name="Test Product", price=100.00)
        self.size = Size.objects.create(name="M")
        self.client = Client()

    def test_add_to_cart_authenticated_user(self):
        self.client.login(username='testuser', password='password')

        
        response = self.client.get(reverse('cart:add_cart', args=[self.product.id]), {'size': self.size.name})
        self.assertEqual(response.status_code, 302)  

        
        cart = Cart.objects.get(cart_id=self.client.session.session_key)
        cart_item = CartItem.objects.get(cart=cart, product=self.product, size=self.size)
        self.assertEqual(cart_item.quantity, 1)

    def test_add_to_cart_not_authenticated(self):
        response = self.client.get(reverse('cart:add_cart', args=[self.product.id]), {'size': self.size.name})
        self.assertRedirects(response, '/login/?next=' + reverse('cart:add_cart', args=[self.product.id]))  
    def test_add_to_cart_invalid_size(self):
        self.client.login(username='testuser', password='password')

        response = self.client.get(reverse('cart:add_cart', args=[self.product.id]), {'size': 'invalid_size'})
        self.assertRedirects(response, reverse('store:all_products'))  

    def test_cart_detail_view(self):
       
        self.client.login(username='testuser', password='password')
        self.client.get(reverse('cart:add_cart', args=[self.product.id]), {'size': self.size.name})

        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')

    def test_cart_remove(self):
        
        self.client.login(username='testuser', password='password')
        self.client.get(reverse('cart:add_cart', args=[self.product.id]), {'size': self.size.name})

        cart = Cart.objects.get(cart_id=self.client.session.session_key)
        cart_item = CartItem.objects.get(cart=cart, product=self.product, size=self.size)

        
        response = self.client.get(reverse('cart:cart_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 0)  

    def test_full_remove(self):
        
        self.client.login(username='testuser', password='password')
        self.client.get(reverse('cart:add_cart', args=[self.product.id]), {'size': self.size.name})

        cart = Cart.objects.get(cart_id=self.client.session.session_key)
        cart_item = CartItem.objects.get(cart=cart, product=self.product, size=self.size)

        
        response = self.client.get(reverse('cart:full_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)

        with self.assertRaises(CartItem.DoesNotExist):
            cart_item.refresh_from_db()

    @patch('stripe.checkout.Session.create')
    def test_cart_checkout_with_loyalty(self, mock_stripe_create):
        
        mock_stripe_create.return_value = {'url': 'http://test.com'}

        
        self.client.login(username='testuser', password='password')
        self.client.get(reverse('cart:add_cart', args=[self.product.id]), {'size': self.size.name})

        
        loyalty_account = Loyalty.objects.create(user=self.user, points=100)

        
        response = self.client.post(reverse('cart:cart_detail'), {'requested_points': 50})

        self.assertEqual(response.status_code, 302)  
        self.assertEqual(loyalty_account.points, 50)  
        mock_stripe_create.assert_called_once()

    def test_empty_cart(self):
        
        self.client.login(username='testuser', password='password')
        self.client.get(reverse('cart:add_cart', args=[self.product.id]), {'size': self.size.name})

        
        response = self.client.get(reverse('cart:empty_cart'))
        self.assertEqual(response.status_code, 302)
        
        
        cart = Cart.objects.get(cart_id=self.client.session.session_key)
        self.assertEqual(cart.cartitem_set.count(), 0)

    @patch('stripe.checkout.Session.retrieve')
    def test_create_order(self, mock_stripe_retrieve):
        
        mock_stripe_retrieve.return_value = {
            'customer_details': {
                'email': 'test@example.com',
                'name': 'Test User',
                'address': {
                    'line1': '123 Main St',
                    'city': 'Test City',
                    'postal_code': '12345',
                    'country': 'US',
                },
            },
            'amount_total': 1000,  
        }

        
        self.client.login(username='testuser', password='password')
        self.client.get(reverse('cart:add_cart', args=[self.product.id]), {'size': self.size.name})

        
        session_id = 'session_id_test'
        response = self.client.get(reverse('cart:create_order') + f'?session_id={session_id}')
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('store:all_products'))  

        
        order = Order.objects.first()
        self.assertEqual(order.emailAddress, 'test@example.com')
        self.assertEqual(OrderItem.objects.count(), 1)

     def test_payment_success(self):
       
        self.client.login(username='testuser', password='password')
        self.client.get(reverse('cart:add_cart', args=[self.product.id]), {'size': self.size.name})

        response = self.client.get(reverse('cart:payment_success'))
        self.assertEqual(response.status_code, 302)  
        loyalty_account = Loyalty.objects.get(user=self.user)
        self.assertEqual(loyalty_account.points, 10)  