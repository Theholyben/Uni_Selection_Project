from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                              username=username, password=password)
            
            if not user:
                raise serializers.ValidationError('Invalid username or password.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            
            # Check if user is student or professor
            if user.role not in ['STUDENT', 'PROFESSOR']:
                raise serializers.ValidationError('Only students and professors can login through this endpoint.')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include "username" and "password".')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id', 'role']

