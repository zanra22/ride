from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Ride, RideEvent
from .serializers import RideSerializer, CreateRideSerializer
from .filters import RideFilter
from .pagination import CustomPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminUser
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from django.db.models import Q, FilteredRelation, Prefetch
# Create your views here.
class RideViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_class = RideFilter
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RideSerializer
        elif self.action in ['create', 'update']:
            return CreateRideSerializer
        return RideSerializer

    def create(self, request, *args, **kwargs):
        #get_serializer specifies the serializer/deserializer to be used.
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                # if valid, save the data and return the response
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error({'Error creating ride': str(e)})
            # if not valid, return the error
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # if not valid, return the error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        # Get all rides
        # select_related performs SQL join and includes the related field. In this case id_rider and id_driver.
        # prefetch_related fetches related Model efficiently using a separate query and caches it.
        # Prefetch today's ride events to optimize performance
        # Changed FilteredRelation to Prefetch and converted it to single QS only.
        current_time = timezone.now()
        queryset = Ride.objects.select_related('id_rider', 'id_driver').prefetch_related(
            Prefetch('rideevent_set',
                     queryset=RideEvent.objects.filter(created_at__gte=current_time - timedelta(hours=24)))
        )
        return queryset
    #Customided list method to include total_count in the response.
    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Add total count to response data for pagination purposes
        response.data['total_count'] = self.paginator.page.paginator.count
        return response