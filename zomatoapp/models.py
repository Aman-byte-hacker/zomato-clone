from django.db import models

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=400)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Resturant(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    image = models.ImageField(upload_to="uploads",default="")
    city = models.CharField(max_length=50,default="")
    status = [
        ('veg','veg'),
        ('Nonveg','Nonveg'),
        ('both','both')
    ]
    base = models.CharField(choices=status,max_length=50,default="")
    mobile = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Dish(models.Model):
    resturant = models.ForeignKey(Resturant,on_delete=models.CASCADE,default="")
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=80)
    image = models.ImageField(upload_to="uploads/dishes",default="",blank=True)
    imagelink = models.CharField(max_length=1400,default="")    
    price = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING,default="")

    def __str__(self):
        return self.name







