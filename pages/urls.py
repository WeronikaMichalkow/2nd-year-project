# pages/urls.py
from django.urls import path, include
from store.views import mens_view # Now the import will work
from .views import homepage,kidspage
from reviews.views import ReviewsView  # Correct import

urlpatterns = [
    path('mens/', mens_view, name='menspage'),
    path('', homepage, name='homepage'),
    path('accounts/', include('accounts.urls')),
    path('reviews/', include('reviews.urls')),
    path('kids/', kidspage, name='kidspage'),
]

