from django.views.generic import TemplateView
from django.shortcuts import render
from store.models import Product, Category


def homepage(request):
    return render(request, "home.html")

def mens_view(request):
    
    men_category = Category.objects.get(name='Men')
    products = Product.objects.filter(category=men_category)
    return render(request, 'mens.html', {'products': products})

def kids_view(request):
    kid_category = Category.objects.get(name='kids')
    products = Product.objects.filter(category=kid_category)
    return render(request, 'kids.html', {'products': products})
    
    





def womens_view(request):
    women_category = Category.objects.get(name='women')
    products = Product.objects.filter(category=women_category)
    return render(request, 'womens.html', {'products': products})
