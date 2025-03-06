from django.urls import path, include
from store.views import mens_view, kids_view, womens_view  # Import for store views
from reviews.views import ReviewsView  # Correct import for reviews
from . import views

urlpatterns = [
    path('mens/', mens_view, name='menspage'),
    path('', views.homepage, name='homepage'),  # Use function-based view
    path('cos_accounts/', include('cos_accounts.urls')),
    path('reviews/', include('reviews.urls')),
    path('kids/', kids_view, name='kidspage'),
    path('womens/', womens_view, name='womenspage'),
]


