from django.contrib import admin
from .models import Product , Review , Order

admin.site.register(Review)
admin.site.register(Order)
admin.site.register(Product)