from django.shortcuts import render
from rest_framework import viewsets
from .models import Ride, RideEvent
from .serializers import RideSerializer
from .filters import RideFilter
from .pagination import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminUser
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from django.db.models import Q, FilteredRelation
# Create your views here.


class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RideFilter
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        # Get all rides
        # select_related performs SQL join and includes the related field. In this case id_rider and id_driver.
        # prefetch_related fetches related Model efficiently using a separate query and caches it.
        queryset = Ride.objects.select_related('id_rider', 'id_driver').prefetch_related('rideevent_set')
        # Prefetch today's ride events to optimize performance
        queryset = queryset.annotate(
            todays_ride_events=FilteredRelation('rideevent_set',
                                                condition=Q(rideevent_set__created_at__gte=timezone.now() - timedelta(hours=24))))
        # count() on the queryset to fetch the total number of objects. Ensures accurate pagination without extra queries.
        self.total_count = queryset.count()
        return queryset

    #Customided list method to include total_count in the response.
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # Add total count to response data for pagination purposes
        response.data['total_count'] = self.total_count
        return response