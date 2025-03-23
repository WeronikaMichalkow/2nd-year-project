from django.shortcuts import redirect, render, get_object_or_404
from store.models import Product, Size
from cart.models import Cart, CartItem 
from django.core.exceptions import ObjectDoesNotExist



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    size_id = request.GET.get('size')

    product = get_object_or_404(Product, id=product_id)

    if not size_id:
        return redirect('store:all_products')  

    try:
        size = get_object_or_404(Size, id=size_id)
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
        size=size  
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

    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


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

