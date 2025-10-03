from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from todos.models import User, Task

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'is_staff', 'is_active']
    search_fields = ['email', 'username']

admin.site.register(User, CustomUserAdmin)
admin.site.register(Task)