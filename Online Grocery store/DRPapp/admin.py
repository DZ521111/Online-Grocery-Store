from django.contrib import admin
from django.contrib import redirects

from .models import Product_details
from .models import product_category
# Register your models here.

admin.site.register(Product_details)
admin.site.register(product_category)