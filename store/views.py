from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Size
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.urls import reverse


def all_products_view(request):
    products = Product.objects.all()
    return render(request, 'all_products.html', {'products': products})


def category_view(request, main_category):
    main_category_obj = get_object_or_404(Category, name__iexact=main_category)
    subcategories = Category.objects.filter(parent=main_category_obj)

    # Capture the subcategory parameter from the URL
    subcategory_name = request.GET.get('subcategory')

    # Show all products if 'all' is selected or if there's no subcategory specified
    if subcategory_name == "all" or not subcategory_name:
        all_categories = [main_category_obj] + list(subcategories)
        products = Product.objects.filter(category__in=all_categories)
    else:
        # Show products in the selected subcategory
        subcategory = get_object_or_404(Category, name__iexact=subcategory_name, parent=main_category_obj)
        products = Product.objects.filter(category=subcategory)

    return render(request, 'category.html', {
        'main_category': main_category_obj,
        'subcategories': subcategories,
        'products': products,
        'selected_subcategory': subcategory_name  # Pass the selected subcategory to the template
    })



def mens_view(request):
    men_category = get_object_or_404(Category, name__iexact="Men")
    subcategories = Category.objects.filter(parent=men_category)

    subcategory_name = request.GET.get('subcategory')

    if subcategory_name:
        subcategory = get_object_or_404(Category, name__iexact=subcategory_name, parent=men_category)
        products = Product.objects.filter(category=subcategory)
    else:
        products = Product.objects.filter(category__in=[men_category] + list(subcategories))

    return render(request, 'mens.html', {
        'products': products,
        'subcategories': subcategories,
    })


def kids_view(request):
    kid_category = get_object_or_404(Category, name__iexact="Kids")
    subcategories = Category.objects.filter(parent=kid_category)

    subcategory_name = request.GET.get('subcategory')

    if subcategory_name:
        subcategory = get_object_or_404(Category, name__iexact=subcategory_name, parent=kid_category)
        products = Product.objects.filter(category=subcategory)
    else:
        products = Product.objects.filter(category__in=[kid_category] + list(subcategories))

    return render(request, 'kids.html', {
        'products': products,
        'subcategories': subcategories,
    })


def womens_view(request):
    women_category = get_object_or_404(Category, name__iexact="Women")
    subcategories = Category.objects.filter(parent=women_category)

    subcategory_name = request.GET.get('subcategory')

    if subcategory_name:
        subcategory = get_object_or_404(Category, name__iexact=subcategory_name, parent=women_category)
        products = Product.objects.filter(category=subcategory)
    else:
        products = Product.objects.filter(category__in=[women_category] + list(subcategories))

    return render(request, 'womens.html', {
        'products': products,
        'subcategories': subcategories,
    })



def add_cart(request, product_id):
    cart = request.session.get('cart', {})

    if product_id in cart:
        cart[product_id] += 1  # Increase quantity if already in cart
    else:
        cart[product_id] = 1  # Add new product with quantity 1

    request.session['cart'] = cart  # Save cart to session
    request.session.modified = True  # Mark session as modified

    return redirect('cart_page')  # Redirect to cart page


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            cart_items.append({'product': product, 'quantity': quantity})
            total_price += product.price * quantity
        except Product.DoesNotExist:
            pass

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})



def stock_management(request):
    """Only superusers can access the stock management page."""
    
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if not logged in

    # Check if the user is a superuser
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-superusers to homepage

    products = Product.objects.all()

    if request.method == "POST":
        product_id = request.POST.get('product_id')
        new_stock = request.POST.get('new_stock')

        try:
            product = Product.objects.get(id=product_id)
            product.quantity_in_stock = int(new_stock)
            product.save()
        except Product.DoesNotExist:
            pass

        return redirect('store:stock_management')

    return render(request, 'stock.html', {'products': products})

# View to add a product
def add_product(request):
    if not request.user.is_superuser:
        return redirect('store:stock_management')

    categories = Category.objects.all()  # Fetch categories for dropdown

    if request.method == "POST":
        name = request.POST.get("name")
        quantity = request.POST.get("quantity")
        price = request.POST.get("price")
        category_id = request.POST.get("category")  # Get selected category ID
        image = request.FILES.get("image")

        if not (name and quantity and price and category_id):
            return render(request, 'store/add.html', {'categories': categories, 'error': "All fields are required!"})

        category = get_object_or_404(Category, id=category_id)  # Get category instance

        new_product = Product(
            name=name,
            quantity_in_stock=quantity,
            price=price,
            category=category,  # Assign the correct category
            image=image
        )
        new_product.save()

        return redirect('store:stock_management')

    return render(request, 'add.html', {'categories': categories})

# View to delete a product
def delete_product(request, product_id):
    if not request.user.is_superuser:
        return redirect('store:stock_management')

    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":  # Ensure deletion only happens on POST request
        product.delete()
        return redirect('store:stock_management')  # Redirect after deletion

    return render(request, 'homepage.html', {'product': product})  # Confirmation page


from django.shortcuts import render
from .models import Product, Category

def filter_list(request):
    products = Product.objects.filter(quantity_in_stock__gt=0)  # Show only in-stock products
    categories = Category.objects.all()
    sizes = Size.objects.all()

    # Get filter parameters from request
    category_filter = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    colour_filter = request.GET.get('colour')
    size_filter = request.GET.get('size')


    colours = Product.objects.values_list('colour', flat=True).distinct()
    

    # Apply filters if parameters exist
    if category_filter and category_filter != "all":
        products = products.filter(category__id=category_filter)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if colour_filter and colour_filter != "all":
        products = products.filter(colour=colour_filter)

    if size_filter and size_filter != "all":
        products = products.filter(sizes__name=size_filter) 

    

    return render(request, 'filter_list.html', {
        'products': products,
        'categories': categories,
        'colours': colours,
        'sizes': sizes,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})



def stock_search(request):
    query = request.GET.get('q', '')  # Default to an empty string if query is None

    if request.method == "POST":
        product_id = request.POST.get('product_id')
        new_stock = request.POST.get('new_stock')

        try:
            product = Product.objects.get(id=product_id)
            product.quantity_in_stock = int(new_stock)
            product.save()
        except Product.DoesNotExist:
            pass

        # Redirect with query appended to the URL
        return redirect('store:stock_management')

    # Perform search only if query is not empty
    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    else:
        products = Product.objects.none()

    return render(request, 'stock.html', {'products': products, 'query': query})