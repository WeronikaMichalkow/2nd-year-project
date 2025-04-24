from django.urls import path
from . import views

app_name='order'

urlpatterns = [
    #path('thank_you/<int:order_id>/', views.thank_you, name='thank_you'),
    path('history/', views.orderHistory.as_view(), name='order_history'),
    
]
