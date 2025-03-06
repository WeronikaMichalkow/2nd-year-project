from django.db import models
from django.conf import settings
from store.models import Product

class Wishlist(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer.username

    class Meta:
        
        constraints = [
            models.UniqueConstraint(fields=['customer', 'product'], name='unique_wishlist_item')
        ]
