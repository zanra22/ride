from django.shortcuts import render
from rest_framework import viewsets
from .models import Ride, RideEvent
from .serializers import RideSerializer
from .filters import RideFilter
from .pagination import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminUser

# Create your views here.


class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    queryset = Ride.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RideFilter
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = CustomPageNumberPagination