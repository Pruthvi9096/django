from django import forms
from .models import Profile,User,Post,Comments

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date','profile_image','mode')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title','content')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('comment',)
        widgets = {
            'comment':forms.Textarea(attrs={'cols':7,'rows':2,'class':'form-control'})
        }