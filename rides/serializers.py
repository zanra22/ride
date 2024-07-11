from rest_framework import serializers
from .models import Ride, RideEvent
from accounts.serializers import UserSerializer


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = '__all__'
class RideSerializer(serializers.ModelSerializer):
    events = RideEventSerializer(many=True, read_only=True, source='rideevent_set')
    todays_ride_events = RideEventSerializer(many=True, read_only=True)
    id_rider = UserSerializer(read_only=True)
    id_driver = UserSerializer(read_only=True)
    class Meta:
        model = Ride
        fields = '__all__'