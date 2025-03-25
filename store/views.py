from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Size, ProductSize
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

    products = Product.objects.prefetch_related("size_stock__size").all()
    sizes = Size.objects.all()

    return render(request, 'stock.html', {'products': products, 'sizes': sizes})

# View to add a product
def add_product(request):
    if not request.user.is_superuser:
        return redirect('store:stock_management')

    categories = Category.objects.all()  # Fetch categories for dropdown
    sizes = Size.objects.all()  # Fetch all sizes

    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        category_id = request.POST.get("category")  # Get selected category ID
        image = request.FILES.get("image")
        colour = request.POST.get("colour")
        quantity = request.POST.get("quantity")

        if not (name and price and category_id and quantity):
            return render(request, 'stock.html', {'categories': categories, 'sizes': sizes, 'error': "All fields are required!"})

        category = get_object_or_404(Category, id=category_id)  # Get category instance

        new_product = Product(
            name=name,
            price=price,
            category=category,
            image=image,
            colour=colour
        )
        new_product.save()

        # Loop over sizes and add the product size stock
        for size in sizes:
            quantity_size = request.POST.get(f"quantity_{size.id}")
            if quantity_size:
                product_size = ProductSize(
                    product=new_product,
                    size=size,
                    quantity=int(quantity_size)
                )
                product_size.save()

        return redirect('store:stock_management')

    return render(request, 'add.html', {'categories': categories, 'sizes': sizes})


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




def update_stock(request):
    # Check if the user is logged in and is a superuser
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not logged in
    if not request.user.is_superuser:
        return redirect('home')  # Show 403 Forbidden page

    if request.method == "POST":
        product_id = request.POST.get('product_id')  # Get the product ID
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return HttpResponseNotFound("Product not found")

        # Loop through all sizes of the product
        for size in product.sizes.all():
            size_field_name = f"size_{size.id}"
            new_stock = request.POST.get(size_field_name)

            # If new stock is provided and is a valid number, update the stock
            if new_stock:
                try:
                    new_stock = int(new_stock)  # Convert to integer
                except ValueError:
                    continue  # If value is not a valid integer, skip this size

                # Check if the product-size entry already exists
                product_size, created = ProductSize.objects.get_or_create(
                    product=product, size=size,
                    defaults={'quantity': new_stock}  # If created, set the initial stock quantity
                )

                if not created:
                    # If the entry already exists, update the quantity
                    product_size.quantity = new_stock
                    product_size.save()

        # After updating, redirect back to the stock management page
        return redirect('store:stock_management')

    return redirect('store:stock_management')  # Redirect if not a POST request

