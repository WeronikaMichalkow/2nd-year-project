from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def mens_view(request):

    men_category = get_object_or_404(Category, name="Men")

   
    subcategories = Category.objects.exclude(name="Men")

    
    subcategory_name = request.GET.get('subcategory')
    if subcategory_name:
        products = Product.objects.filter(category__name=subcategory_name)
    else:
        
        products = Product.objects.filter(category=men_category)

    return render(request, 'mens.html', {
        'products': products,
        'subcategories': subcategories
    })


def category_view(request, main_category):
    # Get the main category (e.g., Men, Women, Kids)
    main_category_obj = get_object_or_404(Category, name__iexact=main_category, parent__isnull=True)

    # Fetch ONLY subcategories under this main category
    subcategories = Category.objects.filter(parent=main_category_obj)

    # Handle subcategory filter
    subcategory_name = request.GET.get('subcategory')

    if subcategory_name == "all" or not subcategory_name:
        # Include products from the main category and its subcategories
        all_categories = [main_category_obj] + list(subcategories)
        products = Product.objects.filter(category__in=all_categories)
    else:
        # Filter by a specific subcategory
        subcategory = get_object_or_404(Category, name__iexact=subcategory_name, parent=main_category_obj)
        products = Product.objects.filter(category=subcategory)

    return render(request, 'category.html', {
        'main_category': main_category_obj,
        'subcategories': subcategories,
        'products': products,
    })
