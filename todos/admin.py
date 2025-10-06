from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from todos.models import User, Task

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ['id', 'email', 'username', 'is_staff', 'is_active']
    search_fields = ['email', 'username']

class CustomTask(admin.ModelAdmin):
    readonly_fields = [ 'id']
    list_display = ['id', 'title', 'get_user_id', 'get_user_username']
    list_filter = ['user']
    
    def get_user_id(self, obj):
        return obj.user.id
    
    get_user_id.short_description = 'User ID'
    get_user_id.admin_order_field = 'user__id'
    
    def get_user_username(self, obj):
        return obj.user
    
    get_user_username.short_description = 'Username'

admin.site.register(User, CustomUserAdmin)
admin.site.register(Task, CustomTask)