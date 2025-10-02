from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class UserRegisterView(APIView):
    
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        """
        Handles POST request for user registration
        """
        serializer = UserRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user)
            return Response(str(token.access_token), status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)