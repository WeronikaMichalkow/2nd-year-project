from django.shortcuts import redirect, render, get_object_or_404
from store.models import Product
from cart.models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist



def _cart_id(request):
    if not request.session.session_key:
        request.session.save()  # Ensures a session ID is created
    return request.session.session_key


def add_cart(request, product_id):
    print(f"Product ID received: {product_id}")  # Debugging

    try:
        product = Product.objects.get(id=product_id)
        print(f"Product found: {product.name}")  # Debugging
    except Product.DoesNotExist:
        print("Product does not exist!")
        print(Product.objects.all())
        return redirect('cart:cart_detail')  

    try:
        cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
        print(f"Cart ID: {cart.cart_id}")  # Debugging
    except Exception as e:
        print(f"Error getting cart: {e}")

    try:
        cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
        if not created and cart_item.quantity < product.stock:
            cart_item.quantity += 1
        cart_item.save()
        print(f"Cart item updated: {cart_item.quantity} of {cart_item.product.name}")  # Debugging
    except Exception as e:
        print(f"Error getting/creating cart item: {e}")

    return redirect('cart:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    print("Loading cart...")  # Debugging

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        print(f"Cart found: {cart.cart_id}, Items: {cart_items.count()}")  # Debugging

        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            counter += cart_item.quantity
            print(f"Cart item: {cart_item.product.name} - Quantity: {cart_item.quantity}")  # Debugging

    except ObjectDoesNotExist:
        print("Cart does not exist!")  # Debugging

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total, 'counter': counter})


def cart_view(request, product_id):
    # Your logic here (you can use main_category if needed)
    context = {
        'product_id': product_id,
    }
    return render(request, 'cart/cart.html', context)  # Adjust path to your template if needed

def cart_remove(request, product_id):
    cart= Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
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

