from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Fields to show in list view
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff']
    
    # Make email clickable
    list_display_links = ['email', 'username']
    
    # Add search
    search_fields = ['email', 'username']
    
    # Add filters
    list_filter = ['is_staff', 'is_active', 'date_joined']
    
    # How fields are grouped in edit form
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )