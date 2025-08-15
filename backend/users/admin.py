from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserPreferences

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email','first_name','last_name','user_type','is_active','is_staff')
    list_filter = ('user_type','is_staff','is_active')
    search_fields = ('email','first_name','last_name')
    ordering = ('email',)

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ('user','email_notifications','preferred_currency')
