from rest_framework import serializers
from account.models import Customer,Product,Order,Category,Tag
from rest_framework.serializers import SerializerMethodField,PrimaryKeyRelatedField

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
    category = CategorySerializer(read_only=True)
    category_id = PrimaryKeyRelatedField(source='category',queryset=Category.objects.all(),write_only=True)
    tags = TagSerializer(many=True,read_only=True)
    tag_ids = PrimaryKeyRelatedField(source='tags',queryset=Category.objects.all(),write_only=True,many=True)
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    product = ProductSerializer()
    class Meta:
        model = Order
        fields = ('customer','product','status')