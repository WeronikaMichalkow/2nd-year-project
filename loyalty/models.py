# loyalty/models.py

from django.db import models
from django.conf import settings

class Loyalty(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='loyalty_account'  
    )
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"Loyalty points for {self.user.username}"
