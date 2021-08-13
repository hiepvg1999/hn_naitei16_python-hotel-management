from django.contrib import admin
from .models import User, Room, RoomImage, Bill, Booking, Service, RoomService, Review

admin.site.register(User)
admin.site.register(Room)
admin.site.register(RoomImage)
admin.site.register(Bill)
admin.site.register(Booking)
admin.site.register(Service)
admin.site.register(RoomService)
admin.site.register(Review)
