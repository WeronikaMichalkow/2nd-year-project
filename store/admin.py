from django.contrib import admin
from .models import Category, Product, Customer

# Register models with the admin panel
admin.site.register(Category )
admin.site.register(Product)
admin.site.register(Customer)





