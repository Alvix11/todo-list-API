from django.urls import path
from .views import UserRegisterView, UserLoginView, TaskCreateView, TaskDetailView, TaskListView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('todos/create', TaskCreateView.as_view(), name='create'),
    path('todos/<int:pk>/', TaskDetailView.as_view(), name='detail'),
    path('todos/<int:pk>/update', TaskUpdateView.as_view(), name='update'),
    path('todos/<int:pk>/delete', TaskDeleteView.as_view(), name='delete'),
    path('todos/', TaskListView.as_view(), name='list'),
]
