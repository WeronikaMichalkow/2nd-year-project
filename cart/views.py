from django.shortcuts import redirect, render, get_object_or_404
from store.models import Product, Size
from cart.models import Cart, CartItem 
from loyalty.models import Loyalty
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from django.urls import reverse
from decimal import Decimal



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
  
 



def cart_detail(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) 
        cart_items = CartItem.objects.filter(cart=cart)  
        total = sum(item.product.price * item.quantity for item in cart_items)  
    except Cart.DoesNotExist:
        cart_items = []
        total = 0

    # Get user's loyalty points and calculate discount
    if request.user.is_authenticated:
        loyalty_account, _ = Loyalty.objects.get_or_create(user=request.user)
        discount = loyalty_account.convert_points_to_discount(total)  # Pass cart total to get the correct discount
    else:
        discount = 0

    final_total = total - discount if total >= discount else 0

    # Stripe Payment Integration
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(final_total * 100)  # Convert to cents
    description = 'Online Shop - New Order'

    if request.method == 'POST':
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'eur',
                        'product_data': {
                            'name': 'Order from Perfect Cushion Shop',
                        },
                        'unit_amount': stripe_total,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                billing_address_collection='required',
                shipping_address_collection={},
                payment_intent_data={'description': description},
                success_url=request.build_absolute_uri(reverse('cart:payment_success')),  
                cancel_url=request.build_absolute_uri(reverse('cart:cart_detail')),    
            )

            # Deduct used points after successful payment
            loyalty_account.points = max(0, loyalty_account.points - int(discount))  # Deduct the discount from points
            loyalty_account.save()

            return redirect(checkout_session.url, code=303)
        except Exception as e:
            return render(request, 'cart.html', {
                'cart_items': cart_items,
                'total': total,
                'discount': discount,
                'final_total': final_total,
                'error': str(e),  
            })

    return render(request, 'cart.html', {
        'cart_items': cart_items, 
        'total': total,
        'discount': discount,
        'final_total': final_total,
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
        loyalty_account.points += 10  # Earn 10 points per purchase
        loyalty_account.save()

    return redirect('store:all_products')  # Redirect to store page after payment
