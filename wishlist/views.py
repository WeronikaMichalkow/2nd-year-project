from django.contrib.auth import get_user_model
from .models import Wishlist
from store.models import Product

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get the current user using the correct model
    customer = get_user_model().objects.get(username=request.user.username)
    Wishlist.objects.get_or_create(customer=customer, product=product)

    return redirect('wishlist:wishlist_view')

def wishlist_view(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(customer=request.user)
    else:
        guest_user = get_user_model().objects.get(username='guest')
        wishlist_items = Wishlist.objects.filter(customer=guest_user)

    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})
