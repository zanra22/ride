from django.shortcuts import render
from rest_framework import viewsets
from .models import Ride, RideEvent
from .serializers import RideSerializer
from .filters import RideFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.


class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    queryset = Ride.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RideFilter