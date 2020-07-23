from django.contrib import admin
from .models import Profile,Following,Post,Comments

admin.site.register(Profile)
admin.site.register(Following)
admin.site.register(Post)
admin.site.register(Comments)
