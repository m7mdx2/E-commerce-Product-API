from django.db import models

# Create your models here.

class category(models.Model):
    name = models.CharField(max_length=100)

class product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.FloatField(blank=False, null=False)
    image_url = models.CharField(max_length=2083)
    description = models.TextField()
    stock_quantity = models.IntegerField(blank=False, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
