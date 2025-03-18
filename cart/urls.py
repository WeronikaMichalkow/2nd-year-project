from django.urls import path, include
from .views import add_cart, cart_view, cart_remove, cart_detail, full_remove
from pages.views import homepage
from . import views

app_name='cart'

urlpatterns = [
    path('add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('', views.cart_detail, name='cart_detail'),
    path('store/<str:main_category>/cart.html', cart_view, name='cart_page'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('full_remove/<int:product_id>/', full_remove, name='full_remove'),
    path('home/', homepage, name='home'),
]