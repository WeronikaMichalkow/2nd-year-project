from django.views.generic import TemplateView
from django.shortcuts import render
from store.models import Product, Category


def homepage(request):
    return render(request, "home.html")

def menspage(request):
    return render(request, "mens.html")

def kidspage(request):
    # Fetch products and subcategories for kids category
    category = Category.objects.get(name='Kids')  # Assuming you have a 'Kids' category
    subcategories = category.subcategory_set.all()  # Assuming subcategories are related to Category
    products = Product.objects.filter(category=category)  # Get all products for the kids category

    return render(request, 'kids.html', {
        'products': products,
        'subcategories': subcategories
    })