from django.contrib import admin
from .models import Task
from django.utils.html import format_html
from django.utils import timezone

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # List view
    list_display = ['title', 'user', 'status_badge', 'priority_badge', 'due_date_display', 'created_at']
    list_filter = ['status', 'priority', 'created_at', 'user']
    search_fields = ['title', 'description', 'user__username', 'user__email']
    
    # Edit form
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'user')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority')
        }),
        ('Dates', {
            'fields': ('due_date', 'completed_at')
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    # Actions
    actions = ['mark_as_completed', 'mark_as_pending']

    # Custom display methods
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'in_progress': 'blue',
            'completed': 'green',
            'cancelled': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="padding: 5px 10px; background-color: {}; color: white; border-radius: 5px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'

    def priority_badge(self, obj):
        colors = {
            'low': 'gray',
            'medium': 'orange',
            'high': 'red'
        }
        color = colors.get(obj.priority, 'gray')
        return format_html(
            '<span style="padding: 5px 10px; background-color: {}; color: white; border-radius: 5px;">{}</span>',
            color,
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'

    def due_date_display(self, obj):
        if not obj.due_date:
            return format_html('<span style="color: gray;">No due date</span>')
        
        if obj.is_overdue():
            return format_html('<span style="color: red;">⏰ Overdue</span>')
        
        return obj.due_date.strftime('%Y-%m-%d')
    due_date_display.short_description = 'Due Date'

    # Custom actions
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} task(s) marked as completed.')
    mark_as_completed.short_description = "Mark selected as completed"

    def mark_as_pending(self, request, queryset):
        updated = queryset.update(status='pending')
        self.message_user(request, f'{updated} task(s) marked as pending.')
    mark_as_pending.short_description = "Mark selected as pending"