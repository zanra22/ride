from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer, CreateUserSerializer
from .permissions import IsAdminUser
from rides.pagination import CustomPageNumberPagination

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return CreateUserSerializer
        return UserSerializer

    def list(self, request, *args, **kwargs):
        try:
            response = super().list(request, *args, **kwargs)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Add total count to response data for pagination purposes
        response.data['total_count'] = self.paginator.page.paginator.count
        return response

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset

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
            logger.error({'Error creating user': str(e)})
            # if not valid, return the error
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # if not valid, return the error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        if 'password' not in data or not data['password']:
            data.pop('password', None)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error({'Error updating user': str(e)})
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)