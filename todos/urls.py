from django.urls import path
from .views import UserRegisterView, UserLoginView, CreateTaskView, UpdateTaskView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('todos/', CreateTaskView.as_view(), name='create'),
    path('todos/<int:pk>/', UpdateTaskView.as_view(), name='update')
]
