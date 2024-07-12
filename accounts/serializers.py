from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'role', 'created_at', 'updated_at', 'id_user']

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'phone_number', 'role', 'admin', 'staff', 'active']
        extra_kwargs = {'password': {'required': False, 'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data['phone_number'],
            role=validated_data['role'],
            admin=validated_data['admin'],
            staff=validated_data['staff'],
            active=validated_data['active']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user