from django.db import models
from django.contrib.auth.models import User
from django.utils import tree
import time
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=400)
    image = models.ImageField(upload_to="uploads/categories",default="")
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Resturant(models.Model):
    
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    image = models.ImageField(upload_to="uploads",default="",blank=False)
    image1 = models.ImageField(upload_to="uploads",default="",blank=False)
    city = models.CharField(max_length=50,default="")
    status = [
        ('veg','veg'),
        ('Nonveg','Nonveg'),
        ('both','both')
    ]
    base = models.CharField(choices=status,max_length=50,default="")
    mobile = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=1000)
    reststatus = [
        ('open','open'),
        ('close','close')
    ]
    reststatus = models.CharField(choices=reststatus,default="",max_length=100)
    timingstart = models.CharField(max_length=100,default="")
    timingend = models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name


class Dish(models.Model):
    resturant = models.ForeignKey(Resturant,on_delete=models.CASCADE,default="")
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=80)
    image = models.ImageField(upload_to="uploads/dishes",default="",blank=True)
    imagelink = models.CharField(max_length=1400,default="",blank=True)    
    price = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING,default="")

    @staticmethod
    def Dishbycategories(categoryid,resturantname):
        if categoryid:
            return Dish.objects.filter(category=categoryid,resturant__name__contains=resturantname.first())
        else:
            return Dish.objects.all()    

    def __str__(self):
        return self.name


class Payment(models.Model):
    dish = models.ForeignKey(Dish,on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    
    statuses = [
        ('success','success'),
        ('fail','fail')
    ]
    payment_id = models.CharField(max_length=400,null=True,blank=True)
    order_id = models.CharField(max_length=400,null=True,blank=True)
    status = models.CharField(choices=statuses,max_length=100)


class Userproduct(models.Model):
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    dish = models.ForeignKey(Dish,on_delete=models.DO_NOTHING)
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE)
    delstatus = [
        ('order accepted','accept'),
        ('Food is being prepared','food is being prepared'),
        ('out for delievery','out for delievery'),
        ('delieverd','delieverd')
    ]
    status = models.CharField(choices = delstatus,max_length=200,default="accepted")	
    date = models.DateTimeField(auto_now_add=True)
