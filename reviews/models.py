from django.conf import settings
from django.db import models

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)  # Allow null for now
    review_text = models.TextField()
    rating = models.PositiveIntegerField(null=True)  # Allow null for now

    def __str__(self):
        return f"Review by {self.user.username if self.user else 'Anonymous'} - Rating: {self.rating}"
