from django.conf import settings
from django.db import models
from store.models import Product  # ✅ Import the correct Product model

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', null=True)
    review_text = models.TextField()
    rating = models.PositiveIntegerField(null=True)

    def __str__(self):
        return f"Review by {self.user.username if self.user else 'Anonymous'} - Rating: {self.rating}"
