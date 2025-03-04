from django.urls import path
from .views import add_to_wishlist, wishlist_view

app_name = 'wishlist'  

urlpatterns = [
    path('add/<int:product_id>/', add_to_wishlist, name='add_to_wishlist'),
    path('', wishlist_view, name='wishlist_view'),
]
