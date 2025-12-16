from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .serializers import LoginSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    Login endpoint for students and professors.
    Returns authentication token and user information.
    """
    serializer = LoginSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Get or create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        # Login user (for session authentication)
        login(request, user)
        
        # Return user data and token
        user_serializer = UserSerializer(user)
        return Response({
            'token': token.key,
            'user': user_serializer.data,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def student_login(request):
    """
    Login endpoint specifically for students.
    """
    serializer = LoginSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Check if user is a student
        if user.role != 'STUDENT':
            return Response({
                'error': 'This endpoint is only for students.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        
        user_serializer = UserSerializer(user)
        return Response({
            'token': token.key,
            'user': user_serializer.data,
            'message': 'Student login successful'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def professor_login(request):
    """
    Login endpoint specifically for professors.
    """
    serializer = LoginSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        
        # Check if user is a professor
        if user.role != 'PROFESSOR':
            return Response({
                'error': 'This endpoint is only for professors.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        
        user_serializer = UserSerializer(user)
        return Response({
            'token': token.key,
            'user': user_serializer.data,
            'message': 'Professor login successful'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
