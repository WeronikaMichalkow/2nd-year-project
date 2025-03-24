from django.shortcuts import redirect, render, get_object_or_404
from store.models import Product, Size
from cart.models import Cart, CartItem 
from loyalty.models import Loyalty
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from django.urls import reverse
from decimal import Decimal
stripe.api_key = settings.STRIPE_SECRET_KEY



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    size_value = request.GET.get('size')  # Can be an ID (1, 2, 3) or a name ('S', 'M', 'L')

    product = get_object_or_404(Product, id=product_id)

    if not size_value:
        return redirect('store:all_products')  

    # Try to determine if size_value is an ID (integer) or a name (string)
    try:
        if size_value.isdigit():  # If size_value is a number, treat it as an ID
            size = get_object_or_404(Size, id=int(size_value))
        else:  # Otherwise, assume it's a size name (e.g., 'S', 'M', 'L')
            size = get_object_or_404(Size, name=size_value)
    except Size.DoesNotExist:
        return redirect('store:all_products')

    if request.user.is_authenticated:
        customer = request.user
    else:
        return redirect('login')  

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=size  # Correct size object
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:cart_detail')  
  
 



# cart/views.py

# cart/views.py

def cart_detail(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart)
        total = sum(item.product.price * item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total = 0

    discount = 0
    final_total = total

    if request.user.is_authenticated:
        loyalty_account, _ = Loyalty.objects.get_or_create(user=request.user)
    else:
        loyalty_account = None

    if request.method == 'POST' and loyalty_account:
        requested_points = int(request.POST.get('requested_points', 0))
        if requested_points > 0:
            discount = loyalty_account.convert_points_to_discount(requested_points, total)

        final_total = total - discount if total >= discount else 0

        loyalty_account.points = max(0, loyalty_account.points - discount)
        loyalty_account.save()

        # Create Stripe Checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Shopping Cart',
                        },
                        'unit_amount': int(final_total * 100),  # Stripe expects the amount in cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri('/cart/success/'),
            cancel_url=request.build_absolute_uri('/cart/cancel/'),
        )

        return redirect(checkout_session.url)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'discount': discount,
        'final_total': final_total,
        'loyalty_points': loyalty_account.points if loyalty_account else 0,
    })

def cart_view(request, product_id):
    
    context = {
        'product_id': product_id,
    }
    return render(request, 'cart/cart.html', context) 

def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    
    
    cart_items = CartItem.objects.filter(product=product, cart=cart)

    if cart_items.exists():
        cart_item = cart_items.first()
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart:cart_detail')


def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart:cart_detail')

def payment_success(request):
    if request.user.is_authenticated:
        loyalty_account, _ = Loyalty.objects.get_or_create(user=request.user)
        
        # Get the total amount spent (adjust accordingly)
        total_amount_spent = request.session.get('total_amount', 0)  # Assuming the total is saved in session
        
        if total_amount_spent > 0:
            # Earn points based on the amount spent
            points_earned = int(total_amount_spent / 10)  # Example: 1 point for every 10 currency units
            loyalty_account.points += points_earned
            loyalty_account.save()

    return redirect('homepage')  # Redirect after payment success

