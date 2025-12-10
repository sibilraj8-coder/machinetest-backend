from rest_framework import serializers
from .models import Task
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    # Computed fields (correct way)
    is_overdue = serializers.SerializerMethodField()
    days_remaining = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'due_date', 'completed_at', 'created_at', 'updated_at',
            'is_overdue', 'days_remaining', 'user'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'completed_at',
            'is_overdue', 'days_remaining', 'user'
        ]

    # Compute if the task is overdue
    def get_is_overdue(self, obj):
        return obj.due_date and obj.due_date < timezone.now() and obj.status != 'completed'

    # Compute days remaining
    def get_days_remaining(self, obj):
        if obj.due_date and obj.status != 'completed':
            delta = obj.due_date - timezone.now()
            return max(delta.days, 0)
        return None

    def validate_due_date(self, value):
        """Ensure due date is not in the past"""
        if value and value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past")
        return value
