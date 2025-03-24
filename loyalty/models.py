from django.db import models
from django.conf import settings  # Import settings

class Loyalty(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='loyalty_account'  
    )
    points = models.IntegerField(default=0)

    def convert_points_to_discount(self):
        return min(self.points * 0.1, 20)  # 10 cents per point, max discount of €20

    def __str__(self):
        return f"Loyalty points for {self.user.username}"
