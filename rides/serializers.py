from rest_framework import serializers
from .models import Ride, RideEvent
from accounts.serializers import UserSerializer
from django.utils import timezone

class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = '__all__'
class RideSerializer(serializers.ModelSerializer):
    events = RideEventSerializer(many=True, read_only=True, source='rideevent_set')
    todays_ride_events = RideEventSerializer(many=True, read_only=True)
    id_rider = UserSerializer(read_only=True)
    id_driver = UserSerializer(read_only=True)

    def validate(self, data):
        # Check if pickup time is in the future for data integrity
        if 'pickup_time' in data:
            if data['pickup_time'] < timezone.now():
                raise serializers.ValidationError('Pickup time cannot be in the past')
        return data
    class Meta:
        model = Ride
        fields = '__all__'

class CreateRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'