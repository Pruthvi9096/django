from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator

class Customer(models.Model):
    name = models.CharField(max_length=200,null=True)
    slug = models.SlugField(null=True,blank=True)
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.name
    
def customer_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    else:
        instance.slug = unique_slug_generator(instance,instance.slug)

pre_save.connect(customer_pre_save_receiver, sender=Customer)


class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    category = models.CharField(max_length=200,null=True)
    price = models.DecimalField(max_digits=7,decimal_places=2,null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=[('pending','Pending'),('ofd','Out For Delivery'),
        ('delivered','Delivered')],max_length=50,default='pending')