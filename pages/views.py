from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Category, Product


class HomeView(TemplateView):
    template_name = 'home.html'

class CategoryView(DetailView):
    model = Category
    template_name = 'pages/category.html'
    context_object_name = 'category'

    def get_object(self):
        return get_object_or_404(Category, id=self.kwargs['category_id'])

class MakeupView(ListView):
    model = Product
    template_name = 'kids.html'
    context_object_name = 'products'

    def get_queryset(self):
        try:
            makeup_category = Category.objects.get(name="Makeup")
            return Product.objects.filter(category=makeup_category)
        except Category.DoesNotExist:
            raise Http404("Makeup category not found.")
