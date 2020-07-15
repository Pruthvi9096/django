from rest_framework import serializers
from account.models import Customer,Product
from rest_framework.serializers import SerializerMethodField

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'