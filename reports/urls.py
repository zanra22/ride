from django.urls import path

from .views import *

urlpatterns = [
    path('report/', get_trip_report),
]