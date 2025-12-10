from django.db import models
from django.conf import settings
from django.utils import timezone

class Task(models.Model):
    # Status choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Priority choices
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    # Basic fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    priority = models.CharField(
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='medium'
    )
    
    # Date fields
    due_date = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    # Auto timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['user', 'due_date']),
        ]

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        # Auto set completed_at when status changes to completed
        if self.pk:
            original = Task.objects.get(pk=self.pk)
            if original.status != 'completed' and self.status == 'completed':
                self.completed_at = timezone.now()
            elif original.status == 'completed' and self.status != 'completed':
                self.completed_at = None
        super().save(*args, **kwargs)

    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and self.status != 'completed':
            return self.due_date < timezone.now()
        return False

    def mark_as_completed(self):
        """Mark task as completed"""
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()