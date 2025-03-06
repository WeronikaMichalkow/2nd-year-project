from django.views.generic import TemplateView
from django.shortcuts import render
from store.models import Product, Category


def homepage(request):
    return render(request, "home.html")

def mens_view(request):
    
    men_category = Category.objects.get(name='Men')
    products = Product.objects.filter(category=men_category)
    return render(request, 'mens.html', {'products': products})

def kidspage(request):
    
    category = Category.objects.get(name='Kids')  
    subcategories = category.subcategory_set.all()  
    products = Product.objects.filter(category=category)  
    return render(request, 'kids.html', {
        'products': products,
        'subcategories': subcategories
    })





def womens_view(request):
    try:
        category = Category.objects.get(name='women')  # Assuming the name is 'women'
        products = Product.objects.filter(category=category)
    except Category.DoesNotExist:
            # Handle the case where the category does not exist
        category = None
        products = []

    return render(request, 'womens.html', {'category': category, 'products': products})