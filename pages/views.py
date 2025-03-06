from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Category, Product

# Homepage view
def homepage(request):
    return render(request, 'home.html')

# Category detail view
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'pages/category.html', {'category': category})

# Makeup category view
def makeup_view(request):
    try:
        makeup_category = Category.objects.get(name="Makeup")
        products = Product.objects.filter(category=makeup_category)
    except Category.DoesNotExist:
        raise Http404("Makeup category not found.")
    
    return render(request, 'kids.html', {'products': products})
