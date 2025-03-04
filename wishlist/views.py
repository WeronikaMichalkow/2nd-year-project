from django.shortcuts import render, redirect, get_object_or_404
from .models import Wishlist
from store.models import Product, Customer


def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    customer = get_object_or_404(Customer, username=request.user.username)

    
    Wishlist.objects.get_or_create(customer=customer, product=product)

    return redirect('wishlist:wishlist_view')


def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        guest_user = User.objects.get(username='guest')
        wishlist_items = Wishlist.objects.filter(user=guest_user)

    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})

