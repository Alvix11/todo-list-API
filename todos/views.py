from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, UserLoginSerializer, TaskSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .utils import get_task_user

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
            refresh = RefreshToken.for_user(user)
            return Response(str(refresh.access_token), status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        """
        Handles POST request for user login
        """
        serializer = UserLoginSerializer(data=request.data)
        
        if serializer.is_valid():
            
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                            'token': str(refresh.access_token)
                            }, 
                            status=status.HTTP_200_OK
                            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TaskCreateView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Handles POST for request create task
        """
        
        serializer = TaskSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        """
        Handles POST for update task
        """
        task = get_task_user(pk, request.user)
        
        if task == 403:
            return Response(
                {"message": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
                )
        elif task == 404:
            return Response(
                {"message": "Not Found"},
                status=status.HTTP_404_NOT_FOUND
                )
        
        serializer = TaskSerializer(task, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Handles DELETE for delete task
        """
        
        task = get_task_user(pk, request.user)
        
        if task == 403:
            return Response(
                {"message": "Forbidden"},
                status=status.HTTP_403_FORBIDDEN
                )

        elif task == 404:
            return Response(
                {"message": "Not Found"},
                status=status.HTTP_404_NOT_FOUND
                )
        
        task.delete()
        return Response(
            {"message": "Success"},
            status=status.HTTP_204_NO_CONTENT
            )