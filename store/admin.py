from django.contrib import admin
from .models import Category, Product, Customer, Size


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent'] 
    search_fields = ['name']  
    list_filter = ['parent']  
    prepopulated_fields = {'name': ('parent',)}  

admin.site.register(Category, CategoryAdmin)


admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Size)






