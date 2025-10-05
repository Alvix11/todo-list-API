from django.urls import path
from .views import UserRegisterView, UserLoginView, TaskCreateView, TaskDetailView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('todos/', TaskCreateView.as_view(), name='create'),
    path('todos/<int:pk>/', TaskDetailView.as_view(), name='update'), 
]
