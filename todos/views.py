from django.shortcuts import render
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
from .serializers import UserRegisterSerializer, UserLoginSerializer, TaskSerializer
from .permissions import IsTaskOwner
from .pagination import CustomPagination
from .utils import get_object
from .models import Task

# Create your views here.
class UserRegisterView(APIView):
    
    authentication_classes = []
    permission_classes = []
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'
    
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
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'auth'
    
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
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'burst'
    
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
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'burst'
        
    def get(self, request, pk):
        """
        Handles GET for show task
        """
        task = get_object(self, pk=pk)

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
        task = get_object(self, pk=pk)
        
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
        task = get_object(self, pk=pk)
        
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
        
        task = get_object(self, pk=pk)
        
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
    throttle_classes = [UserRateThrottle]
    pagination_class = CustomPagination
    
    def get(self, request):
        """
        Handles GET for get task for user
        """
        # Access the query params
        search = request.query_params.get('search')
        username = request.query_params.get('username')
        all_of = request.query_params.get('allof')
        
        if all_of and all_of.lower() == 'true':
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(user=request.user)

        if username and search:
            tasks = tasks.filter(
                (Q(title__icontains=search) |
                Q(description__icontains=search)) & Q(user__username=username)
            )
        
        elif search:
            
            tasks = tasks.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
                )
        
        elif username:
            
            tasks = tasks.filter(
                Q(user__username=username)
                )
        
        tasks = tasks.order_by('id')
        
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(tasks, request)
        serializer = TaskSerializer(result_page, many=True)
        
        return paginator.get_paginated_response(serializer.data)