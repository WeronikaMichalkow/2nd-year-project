from django.shortcuts import render, get_object_or_404
from .models import Product, Category



def category_view(request, main_category):
    main_category_obj = get_object_or_404(Category, name__iexact=main_category)


    subcategories = Category.objects.filter(parent=main_category_obj)


    subcategory_name = request.GET.get('subcategory')

    if subcategory_name == "all" or not subcategory_name:

        all_categories = [main_category_obj] + list(subcategories)
        products = Product.objects.filter(category__in=all_categories)
    else:
        
        subcategory = get_object_or_404(Category, name__iexact=subcategory_name, parent=main_category_obj)
        products = Product.objects.filter(category=subcategory)

    return render(request, 'category.html', {
        'main_category': main_category_obj,
        'subcategories': subcategories,
        'products': products,
    })


def mens_view(request):
    men_category = get_object_or_404(Category, name="Men")
    subcategories = Category.objects.exclude(name="Men")
    subcategory_name = request.GET.get('subcategory')
    
    if subcategory_name:
        products = Product.objects.filter(category__name=subcategory_name)
    else:
        products = Product.objects.filter(category=men_category)

    return render(request, 'pages/mens.html', {
        'products': products,
        'subcategories': subcategories
    })


def kids_view(request):
    # Fetch the 'Kids' category or return a 404 error if not found
    kid_category = get_object_or_404(Category, name="Kids")
    
    # Get all other categories excluding "Kids"
    subcategories = Category.objects.exclude(name="Kids")
    
    # Get the subcategory name from the GET request if provided
    subcategory_name = request.GET.get('subcategory')
    
    # If subcategory is selected, filter products based on it; otherwise, fetch products for 'Kids' category
    if subcategory_name:
        products = Product.objects.filter(category__name=subcategory_name)
    else:
        products = Product.objects.filter(category=kid_category)

    # Return the rendered page with products and subcategories
    return render(request, 'kids.html', {
        'products': products,
        'subcategories': subcategories
    })



def womens_view(request):

    women_category = get_object_or_404(Category, name="Women")

   
    subcategories = Category.objects.exclude(name="Women")

    
    subcategory_name = request.GET.get('subcategory')
    if subcategory_name:
        products = Product.objects.filter(category__name=subcategory_name)
    else:
        
        products = Product.objects.filter(category=women_category)

    return render(request, 'pages/womens.html', {
        'products': products,
        'subcategories': subcategories
    })

