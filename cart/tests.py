from django.test import TestCase
from django.urls import reverse
from store.models import Product
from cart.models import Cart, CartItem

class CartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=10.00,
            stock=10
        )
        self.cart = Cart.objects.create(cart_id="testcart123")
        self.cart_item = CartItem.objects.create(
            product=self.product, cart=self.cart, quantity=1
        )

    def test_cart_add(self):
        response = self.client.get(reverse('cart:add_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to cart detail
        self.assertTrue(CartItem.objects.filter(product=self.product).exists())

    def test_cart_detail_view(self):
        session = self.client.session
        session['cart_id'] = self.cart.cart_id
        session.save()
        
        response = self.client.get(reverse('cart:cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')
        self.assertContains(response, self.product.name)

    def test_cart_remove(self):
        response = self.client.get(reverse('cart:cart_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to cart detail
        cart_item = CartItem.objects.get(product=self.product, cart=self.cart)
        self.assertEqual(cart_item.quantity, 0 if cart_item.quantity == 1 else cart_item.quantity - 1)

    def test_full_remove(self):
        response = self.client.get(reverse('cart:full_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CartItem.objects.filter(product=self.product, cart=self.cart).exists())

