from django.contrib import admin
from .models import Profile,Following,Post,Comments,Main,Attribute

admin.site.register(Profile)
admin.site.register(Following)
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Main)
admin.site.register(Attribute)