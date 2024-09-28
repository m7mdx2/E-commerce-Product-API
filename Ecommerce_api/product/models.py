from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.DecimalField(max_digits=3, decimal_places=2, blank=False, null=False)
    image_url = models.URLField()
    description = models.TextField()
    stock_quantity = models.IntegerField(blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100)
    def __str__(self):
        return self.name
