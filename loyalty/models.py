from django.db import models
from django.conf import settings  # Import settings

class Loyalty(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='loyalty_account'  
    )
    points = models.IntegerField(default=0)

    def convert_points_to_discount(self, cart_total):
        """Calculate discount based on available points and cart total."""
        discount = min(cart_total, self.points)  # Cannot exceed cart total or points available
        return discount

    def __str__(self):
        return f"Loyalty points for {self.user.username}"
