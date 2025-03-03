from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)  # Category name (e.g., Men, Tops, Bottoms)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return f"{self.parent.name} - {self.name}" if self.parent else self.name

    

    


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)

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

class Product(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)

    def __str__(self):
        return self.name




