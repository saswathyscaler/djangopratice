from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserSerializer
from .models import CustomUser
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse

# User registration
@api_view(['POST'])
def register(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User login
@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)
    
    if user is not None:
        login(request, user)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    return Response({'detail': 'Authentication failed.'}, status=status.HTTP_401_UNAUTHORIZED)

# User profile editing
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_profile(request):
    serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# User deletion
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    user = request.user
    user.delete()
    return Response({'detail': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
