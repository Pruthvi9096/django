from django.contrib import admin
from .models import Profile,Following,Post,Comments,Group,Member,Membership,Event,Usage

admin.site.register(Profile)
admin.site.register(Following)
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Group)
admin.site.register(Member)
admin.site.register(Membership)
admin.site.register(Event)
admin.site.register(Usage)