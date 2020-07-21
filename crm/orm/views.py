from django.shortcuts import render
from .models import Category,Product
from django.http import JsonResponse
import random
import string
import time
import json
from django.db.models import Max,Count,F

def orm_practice(request):
    category = Category.objects.all().annotate(product_count=Count('product'))[:20]
    category = Category.objects.all().update(name=F('name') + '1')
    for c in category:
        print(c.product_count)
    return JsonResponse("Hello",safe=False)