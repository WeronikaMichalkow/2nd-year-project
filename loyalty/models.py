# loyalty/models.py
from django.db import models
from django.conf import settings  # Import settings

class Loyalty(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='loyalty_account'  
    )
    points = models.IntegerField(default=0)

    def convert_points_to_discount(self, requested_points, cart_total):
        """Calculate discount based on requested points and cart total."""
        # The discount is limited by the total cart value and the user's available points
        points_to_apply = min(requested_points, self.points, cart_total)
        return points_to_apply

    def __str__(self):
        return f"Loyalty points for {self.user.username}"
