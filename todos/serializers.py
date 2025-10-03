from rest_framework import serializers
from todos.models import User, Task
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
    def create(self, validated_data):
        
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        
        return user

class UserLoginSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        
        email = data.get('email')
        password = data.get('password')
        
        user = authenticate(email=email, password=password)
        
        if not user:
            raise serializers.ValidationError("Credentials error")
        
        data['user'] = user
        return data
    
class TaskSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description']