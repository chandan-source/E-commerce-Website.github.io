from django.db import models
from django.contrib.auth.models import User
from datetime import date,timedelta
# Create your models here.
status=[["order_confirmed","order_confirmed"],
        ["shipped",'shipped'],
        ["out_for_delivery","out_for_delivery"],
        ["delivered","delivered"]]
class category(models.Model):
    name=models.CharField(max_length=100,null=True)

    def __str__(self):
       return self.name

class subcategory(models.Model):
    cat=models.ForeignKey(category,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.name+"--"+self.cat.name

class product(models.Model):
    subcat=models.ForeignKey(subcategory,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=100,null=True)
    price=models.IntegerField(null=True)
    stock=models.IntegerField(null=True)
    img1=models.FileField(null=True)
    img2=models.FileField(null=True)
    img3=models.FileField(null=True)
    des=models.TextField(null=True)
    size=models.CharField(max_length=100,null=True,blank=True)
    rate=models.IntegerField(null=True)

    def __str__(self):
        return self.name+"--"+self.subcat.name

class user_detail(models.Model):
    usr=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    mobile=models.IntegerField(null=True)
    img=models.FileField(null=True)
    address=models.TextField(null=True)
    def __str__(self):
        return self.usr.username

class Cart(models.Model):
    usr=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    pro=models.ForeignKey(product,on_delete=models.CASCADE,null=True)
    quatity=models.IntegerField(null=True)
    total_price=models.IntegerField(null=True)
    size=models.CharField(null=True,max_length=100,blank=True)
    def __str__(self):
        return self.usr.username
class order_product(models.Model):
    usr=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    order_id=models.CharField(max_length=100,null=True,blank=True)
    fullname=models.CharField(max_length=100,null=True)
    house_no=models.CharField(max_length=100,null=True)
    area_name=models.CharField(max_length=100,null=True)
    city_state=models.CharField(max_length=100,null=True)
    landmark=models.CharField(max_length=100,null=True,blank=True)
    pincode=models.CharField(max_length=100,null=True)
    mobile1=models.CharField(max_length=100,null=True)
    mobile2=models.CharField(max_length=100,null=True)
    payment_id=models.CharField(max_length=100,null=True,blank=True)
    payment_status = models.CharField(max_length=100, null=True, default="not done", blank=True)
    amount = models.IntegerField(null=True, blank=True)
    order_date=models.DateField(null=True,blank=True)
    def __str__(self):
        return self.fullname
class order_product_detail(models.Model):
    order_detail=models.ForeignKey(order_product,on_delete=models.CASCADE,null=True)
    pro = models.ForeignKey(product, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=100, null=True, choices=status, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    totalprice = models.IntegerField(null=True, blank=True)
    expected_date=models.DateField(null=True,blank=True)
    def __str__(self):
        return self.pro.name










