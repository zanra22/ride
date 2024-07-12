from django.urls import path

from .views import *

urlpatterns = [
    path('ride/<int:pk>/', RideViewSet.as_view({'get': 'retrieve'})),
    path('ride/', RideViewSet.as_view({'get': 'list', 'post': 'create'})),
]