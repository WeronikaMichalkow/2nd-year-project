from django.views.generic import TemplateView
from django.shortcuts import render
from store.models import Product, Category

# Create your views here.

def homepage(request):
    return render(request, "home.html")

def menspage(request):
    return render(request, "mens.html")

def kids_view(request):
    return render(request, 'kids.html')
