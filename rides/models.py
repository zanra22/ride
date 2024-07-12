from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from datetime import datetime
from datetime import timedelta

User = get_user_model()

# Create your models here.

class Ride(models.Model):
    id_ride = models.AutoField(primary_key=True)
    status_choices = (('en-route', 'en-route'), ('pickup', 'pickup'), ('dropoff', 'dropoff'))
    status = models.CharField(max_length=50, choices=status_choices)
    id_rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rider')
    id_driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver')
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField(auto_now_add=False)
    dropoff_time = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return str(self.id_ride)

    def todays_ride_events(self):
        # Calculate the datetime range for the last 24 hours
        start_time = timezone.now() - timedelta(hours=24)
        # Retrieve RideEvents occurred within the last 24 hours related to this Ride
        return self.rideevent_set.filter(created_at__gte=start_time)


class RideEvent(models.Model):
    id_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey('rides.Ride', on_delete=models.CASCADE, related_name='rideevent_set')
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id_event)

