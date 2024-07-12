from django.urls import path

from .views import *

urlpatterns = [
    path('ride/<int:pk>/', RideViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('ride/', RideViewSet.as_view({'get': 'list', 'post': 'create'})),
]