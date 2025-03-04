from django.contrib import admin
<<<<<<< HEAD
from .models import Category, Product, Customer

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')  # Display name and parent category in the list
    list_filter = ('parent',)  # Add filtering by parent category
    search_fields = ('name',)  # Enable search by name
=======
from .models import Product, Category, Customer
>>>>>>> Weronika

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price')  # Display product details in the list view
    list_filter = ('category',)  # Filter products by category
    search_fields = ('name',)  # Enable search by product name

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'category_preference')  # Display customer details
    search_fields = ('username', 'name')  # Enable search by username and name

# Register models with the admin panel
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)





