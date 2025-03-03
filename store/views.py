from django.shortcuts import render, get_object_or_404
from .models import Product, Category

# View to display products under the 'Men' category
def mens_view(request):
    # Get the "Men" category
    men_category = get_object_or_404(Category, name="Men")

    # Get all subcategories related to "Men"
    subcategories = Category.objects.exclude(name="Men")

    # Filter products by selected subcategory (if provided)
    subcategory_name = request.GET.get('subcategory')
    if subcategory_name:
        products = Product.objects.filter(category__name=subcategory_name)
    else:
        # Show all products for Men if no subcategory is selected
        products = Product.objects.filter(category=men_category)

    return render(request, 'mens.html', {
        'products': products,
        'subcategories': subcategories
    })





def category_view(request, main_category):
    # Get the main category (e.g., Men, Women, Kids)
    main_category_obj = get_object_or_404(Category, name__iexact=main_category, parent__isnull=True)

    # Get all subcategories under this main category
    subcategories = main_category_obj.subcategories.all()

    # Check if a subcategory filter is applied
    subcategory_name = request.GET.get('subcategory')

    if subcategory_name:
        # Show products only for the selected subcategory
        subcategory = get_object_or_404(Category, name=subcategory_name, parent=main_category_obj)
        products = Product.objects.filter(category=subcategory)
    else:
        # Include products from the main category AND its subcategories
        all_categories = [main_category_obj] + list(subcategories)
        products = Product.objects.filter(category__in=all_categories)

    return render(request, 'category.html', {
        'main_category': main_category_obj,
        'subcategories': subcategories,
        'products': products,
    })