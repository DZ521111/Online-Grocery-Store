from django.db import models
import numpy as np

class product_category(models.Model):
    category_name=models.CharField(max_length=200)
    image=models.ImageField(upload_to='pics')


class add_to_cart(models.Model):
    id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=30)
    product_name=models.CharField(max_length=30)
    quantity = models.IntegerField(default=0)

class Product_details(models.Model):
    product_name = models.CharField(max_length=30)
    category_name = models.CharField(max_length=20)
    product_img1 = models.ImageField(upload_to='pics')
    product_img2 = models.ImageField(upload_to='pics')
    product_description = models.TextField(max_length=5000,null=True)
    product_price = models.IntegerField()
    product_expirydate = models.DateField(null=True)
    product_manufecturingdate = models.DateField(null=True)
    quantity = models.IntegerField(default=10)

class bill(models.Model):
    username = models.CharField(max_length=30,default='')
    total_bill=models.IntegerField(default=0)




