from django.db import models
from django.conf import settings  

class Loyalty(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='loyalty_account'  
    )
    points = models.IntegerField(default=0)

    def convert_points_to_discount(self, requested_points, cart_total):
        """Calculate the discount based on requested points and the cart total."""
        points_to_apply = min(requested_points, self.points, cart_total)

       
        cashback_points = int(points_to_apply * 0.1)  

        return points_to_apply, cashback_points

    def __str__(self):
        return f"Loyalty points for {self.user.username}"