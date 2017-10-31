from django.contrib import admin
from .models import Location, Building, Room, Address
# Register your models here.

admin.site.register(Location)
admin.site.register(Room)
admin.site.register(Building)
admin.site.register(Address)