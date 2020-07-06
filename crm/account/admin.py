from django.contrib import admin
from .models import Customer,Order,Product,Category,Tag

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)