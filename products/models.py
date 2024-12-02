from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    # Image fields
    thumbnail = models.ImageField(upload_to='product_images/', null=True)
    mobile_image = models.ImageField(upload_to='product_images/', null=True)
    tablet_image = models.ImageField(upload_to='product_images/', null=True)
    desktop_image = models.ImageField(upload_to='product_images/', null=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        return self.product.price * self.quantity