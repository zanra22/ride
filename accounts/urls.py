from django.urls import path

from .views import *

urlpatterns = [
    path('user/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('user/', UserViewSet.as_view({'get': 'list', 'post': 'create'})),
]