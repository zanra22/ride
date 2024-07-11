from django.contrib.auth import get_user_model
from django.db import models
# from accounts.models import User

User = get_user_model()

# Create your models here.

class Ride(models.Model):
    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50) #('en-route', 'pickup', 'dropoff')
    id_rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rider')
    id_driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='driver')
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return str(self.id_ride)


class RideEvent(models.Model):
    id_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey('rides.Ride', on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id_event)

