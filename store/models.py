from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return f"{self.parent.name} - {self.name}" if self.parent else self.name


class Size(models.Model):
    name = models.CharField(max_length=50)  

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    sizes = models.ManyToManyField(Size, related_name='products') 
    quantity_in_stock = models.PositiveIntegerField(default=0)
    colour = models.CharField(max_length=50, blank=True, null=True)  

    def __str__(self):
        return self.name


class Customer(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email_address = models.CharField(max_length=255)
    category_preference = models.CharField(max_length=255)

    def __str__(self):
        return self.username
