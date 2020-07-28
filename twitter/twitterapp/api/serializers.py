from rest_framework import serializers
from ..models import Profile,Post,Following,Comments,User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','email')

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        exclude = ['followers']

    def update(self,instance,validated_data):
        user_data = dict(validated_data.pop('user'))
        instance.user.first_name = user_data.get('first_name', instance.user.first_name)
        instance.user.last_name = user_data.get('last_name', instance.user.last_name)
        instance.user.email = user_data.get('email', instance.user.email)
        instance.save()
        return super(ProfileSerializer,self).update(instance=instance,validated_data=validated_data)

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.user.username')
    class Meta:
        model = Post
        fields = ('author','title','content')