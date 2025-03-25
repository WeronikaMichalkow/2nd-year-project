from django.contrib import admin
from .models import Category, Product, Customer, Size, ProductSize

# Category Admin
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent'] 
    search_fields = ['name']  
    list_filter = ['parent']  

admin.site.register(Category, CategoryAdmin)

# Inline Admin for ProductSize
class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1  
    fields = ['size', 'quantity']  
    min_num = 1  


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity_in_stock')  # Customize the list view
    search_fields = ('name',)  # Allow search by product name
    list_filter = ('category',)  # Filter by category in the admin list view
    inlines = [ProductSizeInline]  # Add ProductSizeInline to allow size stock editing


admin.site.register(Product, ProductAdmin)
admin.site.register(Customer)
admin.site.register(Size)
admin.site.register(ProductSize)






