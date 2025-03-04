from django.contrib import admin
from .models import Wishlist

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'added_at')  # Fields displayed in the admin list view
    search_fields = ('customer__username', 'product__name')  # Search functionality for users & products

admin.site.register(Wishlist, WishlistAdmin)
