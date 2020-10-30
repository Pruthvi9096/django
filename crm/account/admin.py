from django.contrib import admin
from .models import Customer,Order,Product,Category,Tag,Leave,Location,TrackingData,Galaxy,Star,Itinerary, Tour

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Leave)

admin.site.register(Location)
admin.site.register(TrackingData)

admin.site.register(Galaxy)
admin.site.register(Star)

admin.site.register(Itinerary)
admin.site.register(Tour)