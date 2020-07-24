from django.contrib import admin
from .models import Profile,Following,Post,Comments,People,Rating

admin.site.register(Profile)
admin.site.register(Following)
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(People)
admin.site.register(Rating)
