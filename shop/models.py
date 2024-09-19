from django .contrib.auth.models import User
from django.db import models
import datetime
import os
# Create your models here.
def getFileName(request,filename):
    now_time = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)

class Catagory(models.Model):
    Catagory_Name=models.CharField(max_length=150,null=False,blank=False)
    Catagory_Image = models.ImageField(upload_to=getFileName,null=True,blank=True)
    Catagory_Description=models.TextField(max_length=200,null=False,blank=False)
    Status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    Created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.Catagory_Name
 

class Products(models.Model):
    Catagory=models.ForeignKey(Catagory,on_delete=models.CASCADE)
    Product_Name=models.CharField(max_length=150,null=False,blank=False)
    Product_Vender=models.CharField(max_length=150,null=False,blank=False)
    Product_Image = models.ImageField(upload_to=getFileName,null=True,blank=True)
    Quantity=models.IntegerField(null=False,blank=False)
    Original_price=models.FloatField(null=False,blank=False)
    Selling_price=models.FloatField(null=False,blank=False)
    Product_Description=models.TextField(max_length=200,null=False,blank=False)
    Status=models.BooleanField(default=False,help_text="0-show,1-Hidden")
    Trending_product=models.BooleanField(default=False,help_text="0-default,1-Trending")
    Created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.Product_Name      
    
from django.db import models
from django.contrib.auth.models import User
from .models import Products

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False, blank=False)
    product_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total price of the product
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} ({self.product_qty}) - {self.user}'
