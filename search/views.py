from django.shortcuts import render
from store.models import Product
from django.db.models import Q

def search_results(request):
    query = request.GET.get('q')

    # If a query exists, filter products by name or description
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.none()  # Return empty queryset if no search term

    return render(request, 'search.html', {'products': products, 'query': query})
