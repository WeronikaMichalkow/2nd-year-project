# pages/urls.py
from django.urls import path, include
from store.views import mens_view,kids_view # Now the import will work
from .views import homepage
from reviews.views import ReviewsView  # Correct import
from . import views

urlpatterns = [
    path('mens/', mens_view, name='menspage'),
    path('', homepage, name='homepage'),
    path('cos_accounts/', include('cos_accounts.urls')),
    path('reviews/', include('reviews.urls')),
    path('kids/', kids_view, name='kidspage'),
    path('', views.HomePageView.as_view(), name='home'),
]

