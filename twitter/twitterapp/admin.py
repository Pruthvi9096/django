from django.contrib import admin
from .models import Profile,Following,Post,Comments,AccountsInsightsHourly,Author,Book
admin.site.register(Profile)
admin.site.register(Following)
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(AccountsInsightsHourly)
admin.site.register(Author)
admin.site.register(Book)