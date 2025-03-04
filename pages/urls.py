from django.urls import path
from store.views import mens_view
from .views import homepage

urlpatterns = [
    path('mens/', mens_view, name='menspage'),
    path('', homepage, name='homepage'),
]
