from rest_framework import serializers
from ..models import Attribute,Main

class MainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Main
        fields = '__all__'

class AttributeSerializer(serializers.ModelSerializer):
    main = MainSerializer(read_only=True)
    main_id = serializers.PrimaryKeyRelatedField(source='main',  queryset=Main.objects.all(), write_only=True)
    class Meta:
        model = Attribute
        fields = '__all__'
        

class AttributeGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'
        depth = 2