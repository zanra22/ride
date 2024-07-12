from django.urls import path

from .views import *

urlpatterns = [
    path('ride/<int:pk>/', RideViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('ride/', RideViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('ride/<int:pk>/event/', RideEventViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('ride/<int:pk>/event/<int:event_pk>/', RideEventViewSet.as_view({'get': 'retrieve',
                                                                          'put': 'update',
                                                                          'delete': 'destroy'
                                                                          })),
]