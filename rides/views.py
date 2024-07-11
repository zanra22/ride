from django.shortcuts import render
from rest_framework import viewsets
from .models import Ride
from .serializers import RideSerializer
# Create your views here.


class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    def get_queryset(self):
        return Ride.objects.all()