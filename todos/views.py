from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, UserLoginSerializer, TaskSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .permissions import IsTaskOwner
from rest_framework_simplejwt.authentication import JWTAuthentication
from .pagination import CustomPagination
from .models import Task

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
            return Response({
                            'token': str(refresh.access_token)
                            }, 
                            status=status.HTTP_201_CREATED
                            )
        
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
    permission_classes = [IsAuthenticated, IsTaskOwner]
    
    def get_object(self, pk):
        """
        Obtain task and verify permissions
        """
        try:
            task = Task.objects.get(pk=pk)
            self.check_object_permissions(self.request, task)
            return task
        except Task.DoesNotExist:
            return None
        
    def get(self, request, pk):
        """
        Handles GET for show task
        """
        task = self.get_object(pk=pk)

        if task is None:
            return Response(
                {"message": "Not Found"},
                status=status.HTTP_404_NOT_FOUND
                )
        
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, pk):
        """
        Handles POST for update task
        """
        task = self.get_object(pk=pk)
        
        if task is None:
            return Response(
                {"message": "Not Found"},
                status=status.HTTP_404_NOT_FOUND
                )
        
        serializer = TaskSerializer(task, data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        """
        Handles PATCH for update task
        """
        task = self.get_object(pk=pk)
        
        if task is None:
            return Response(
                {"message": "Not Found"},
                status=status.HTTP_404_NOT_FOUND
                )
        
        serializer = TaskSerializer(task, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        Handles DELETE for delete task
        """
        
        task = self.get_object(pk=pk)
        
        if task is None:
            return Response(
                {"message": "Not Found"},
                status=status.HTTP_404_NOT_FOUND
                )
        
        task.delete()
        return Response(
            {"message": "Success"},
            status=status.HTTP_204_NO_CONTENT
            )

class TaskListView(APIView):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    
    def get(self, request):
        """
        Handles GET for get task for user
        """
        tasks = Task.objects.all().order_by('id')
        
        paginator = self.pagination_class()
        
        result_page = paginator.paginate_queryset(tasks, request)
        
        serializer = TaskSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)