from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from store.models import Customer

class Question(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # User who asked the question
    text = models.TextField()
    answer = models.TextField(blank=True, null=True)  
    created = models.DateTimeField(auto_now_add=True)
    answered = models.DateTimeField(null=True, blank=True)

    def __str__(self):  
        return "Question by " + str(self.customer)
