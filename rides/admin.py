from django.contrib import admin

from .models import Ride, RideEvent
# Register your models here.


admin.site.register(Ride)
admin.site.register(RideEvent)
