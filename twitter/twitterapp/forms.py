from django import forms
from .models import Profile,User,Post

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date','profile_image')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','content')