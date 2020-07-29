from rest_framework import serializers
from ..models import Profile,Post,Following,Comments,User

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = '__all__'
    
    def validate(self,validated_data):
        target = validated_data.get('target')
        follower = validated_data.get('follower')
        if target == follower:
            raise serializers.ValidationError("Self Following is not allowed!")
        return super(FollowingSerializer,self).validate(validated_data)

class GetFollowerSerializer(serializers.ModelSerializer):
    followers = UserSerializer(read_only=True,source='follower')
    class Meta:
        model = Following
        fields = ('followers',)

class GetFollowingSerializer(serializers.ModelSerializer):
    followings = UserSerializer(read_only=True,source='target')
    class Meta:
        model = Following
        fields = ('followings',)

class ParentCommentSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user',queryset=User.objects.all(),write_only=True)
    post_id = serializers.PrimaryKeyRelatedField(source='post',queryset=Post.objects.all(),write_only=True)
    user = serializers.CharField(read_only=True,source='user.username')
    class Meta:
        model = Comments
        fields = ('comment','user','user_id','post_id')

class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='user',queryset=User.objects.all(),write_only=True)
    post_id = serializers.PrimaryKeyRelatedField(source='post',queryset=Post.objects.all(),write_only=True)
    parent_comment_id = serializers.PrimaryKeyRelatedField(source='parent_comment',queryset=Comments.objects.all(),write_only=True)
    user = serializers.CharField(read_only=True,source='user.username')
    comments_set = ParentCommentSerializer(many=True, read_only=True)
    class Meta:
        model = Comments
        fields = ('comment','user','user_id','post_id','comments_set','parent_comment_id')
    
    def get_fields(self, *args, **kwargs):
        fields = super(CommentSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields['user_id'].read_only = True
            fields['post_id'].read_only = True
        return fields
    

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Profile
        exclude = ['followers',]

    def update(self,instance,validated_data):
        user_data = dict(validated_data.pop('user'))
        instance.user.first_name = user_data.get('first_name', instance.user.first_name)
        instance.user.last_name = user_data.get('last_name', instance.user.last_name)
        instance.user.email = user_data.get('email', instance.user.email)
        instance.save()
        return super(ProfileSerializer,self).update(instance=instance,validated_data=validated_data)

class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.PrimaryKeyRelatedField(source='author',queryset=Profile.objects.all(),write_only=True)
    author = serializers.ReadOnlyField(source='author.user.username')
    comments_set = CommentSerializer(many=True,read_only=True)
    class Meta:
        model = Post
        fields = ('author','author_id','title','content','comments_set')
    
    def get_fields(self, *args, **kwargs):
        fields = super(PostSerializer, self).get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields['author_id'].read_only = True
        return fields

class OnlyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['followers',]

class UserProfileSerializer(serializers.ModelSerializer):
    profile = OnlyProfileSerializer()
    class Meta:
        model = User
        exclude = ['password',]

class UserAuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'