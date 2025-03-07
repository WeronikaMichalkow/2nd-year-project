from django.shortcuts import render, get_object_or_404
from .models import Product, Category



def all_products_view(request):
    products = Product.objects.all()
    # Your logic for displaying all products
    return render(request, 'all_products.html', {'products': products})



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
    
    kid_category = get_object_or_404(Category, name="Kids")
    
   
    subcategories = Category.objects.exclude(name="Kids")
    
 
    subcategory_name = request.GET.get('subcategory')
    

    if subcategory_name:
        products = Product.objects.filter(category__name=subcategory_name)
    else:
        products = Product.objects.filter(category=kid_category)

  
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
