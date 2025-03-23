from django.shortcuts import render
from store.models import Product
from django.db.models import Q

def search_results(request):
    query = request.GET.get('q')  # Get the search query from the URL parameters
    
    if query:
        # Split the query into words
        search_terms = query.split()

        # Initialize an empty Q object for combining queries
        query_filter = Q()

        # For each word, create a Q object that searches for it in the product name or description
        for term in search_terms:
            query_filter |= Q(name__icontains=term) | Q(description__icontains=term)

        # Apply the filter to the Product model
        products = Product.objects.filter(query_filter)
    else:
        # If no query is provided, return no products
        products = Product.objects.none()  

    return render(request, 'search.html', {'products': products, 'query': query})
