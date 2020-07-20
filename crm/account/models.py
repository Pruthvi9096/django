from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .utils import unique_slug_generator

class Customer(models.Model):
    name = models.CharField(max_length=200,null=True)
    slug = models.SlugField(null=True,blank=True)
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.name or ''
    
def customer_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(customer_pre_save_receiver, sender=Customer)

class Category(models.Model):
    name = models.CharField(max_length=250,null=True)
    description = models.TextField(max_length=700,null=True,blank=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=250,null=True)

    def __str__(self):
        return self.name or ''

class Product(models.Model):
    name = models.CharField(max_length=200,null=True)
    description = models.TextField(max_length=700,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    tags = models.ManyToManyField(Tag)
    price = models.DecimalField(max_digits=7,decimal_places=2,null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or ''

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=[('pending','Pending'),('ofd','Out For Delivery'),
        ('delivered','Delivered')],max_length=50,default='pending')
    
    def __str__(self):
        return '{}-{}'.format(self.customer.name,self.product.name) or ''