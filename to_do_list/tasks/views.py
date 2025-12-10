from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    # Enable filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'due_date']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return tasks for the logged-in user only"""
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Assign the logged-in user to the task"""
        serializer.save(user=self.request.user)

    # Mark task as completed
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        task = self.get_object()
        task.mark_as_completed()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    # Get overdue tasks
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        tasks = self.get_queryset().filter(
            due_date__lt=timezone.now(),
            status__in=['pending', 'in_progress']
        )
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    # Get task statistics
    @action(detail=False, methods=['get'])
    def stats(self, request):
        tasks = self.get_queryset()
        total = tasks.count()
        completed = tasks.filter(status='completed').count()
        pending = tasks.filter(status='pending').count()
        in_progress = tasks.filter(status='in_progress').count()

        return Response({
            'total_tasks': total,
            'completed': completed,
            'pending': pending,
            'in_progress': in_progress,
            'completion_rate': round((completed / total * 100), 2) if total > 0 else 0
        })
