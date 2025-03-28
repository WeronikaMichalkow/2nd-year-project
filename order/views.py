from django.shortcuts import render, redirect
from .models import Order

def order_history(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    
    orders = Order.objects.filter(emailAddress=request.user.email)

    return render(request, 'order/order_history.html', {'orders': orders})



