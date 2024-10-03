from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    image_url = models.URLField()
    description = models.TextField()
    stock_quantity = models.IntegerField(default = 0,blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()  # Number of units ordered
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user}"

    def save(self, *args, **kwargs):
        # Check if there's enough stock before placing the order
        if self.product.stock_quantity < self.quantity:
            raise ValidationError(f"Not enough stock for {self.product.name}. Available stock is {self.product.stock_quantity}.")

        # Reduce stock quantity after order is placed
        self.product.stock_quantity -= self.quantity
        self.product.save()

        super().save(*args, **kwargs)
class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s review of {self.product.name}"
class Category(models.Model):
    name = models.CharField(max_length=100, null = False, blank = False)

    def __str__(self):
        return self.name