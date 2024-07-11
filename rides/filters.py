import django_filters
from .models import Ride
from django.contrib.auth import get_user_model

User = get_user_model()

class RideFilter(django_filters.FilterSet):
    rider_email = django_filters.CharFilter(lookup_expr='iexact', field_name='id_rider__email')
    class Meta:
        model = Ride
        fields = ['status', 'rider_email']
