from django.urls import path, include
from store.views import mens_view, kids_view, womens_view  
from reviews.views import ReviewsView  
from . import views

urlpatterns = [
    path('store/men/', views.mens_view, name='mens'),
    path('', views.homepage, name='homepage'),  
    path('cos_accounts/', include('cos_accounts.urls')),
    path('reviews/', include('reviews.urls')),
    path('kids/', kids_view, name='kidspage'),
    path('store/women/', views.womens_view, name='womens'),

]


