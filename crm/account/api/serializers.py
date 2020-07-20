from rest_framework import serializers
from account.models import Customer,Product,Order,Category,Tag
from rest_framework.serializers import SerializerMethodField

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=False, read_only=True)
    tags = TagSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    product = ProductSerializer()
    class Meta:
        model = Order
        fields = ('customer','product','status')