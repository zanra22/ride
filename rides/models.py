from django.db import models

# Create your models here.

class Ride(models.Model):
    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50) #('en-route', 'pickup', 'dropoff')
    id_rider = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='rider')
    id_driver = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='driver')
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return str(self.id_ride)

