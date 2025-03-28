from django.urls import path
from .views import order_history

app_name='order'

urlpatterns = [
    path('order/', order_history, name='order_history'),
]
