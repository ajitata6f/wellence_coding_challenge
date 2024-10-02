from datetime import datetime

from django.conf import settings
from django.db import models

from tasks.enums import TaskPriority


# Create your models here.
class Task(models.Model):
    PRIORITY_CHOICES = [
        (priority.value, priority.name) for priority in TaskPriority
    ]

    user_email = models.EmailField(unique=True)
    task = models.CharField(max_length=200)
    due_by = models.DateTimeField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES)
    is_urgent = models.BooleanField(default=False)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tasks'
        ordering = ['task']
        indexes = [
            models.Index(fields=['id']),
            models.Index(fields=['task']),
            models.Index(fields=['-created_at']),
        ]

    def is_due(self):
        # Check if the task is due
        return self.due_by <= datetime.now()

    def __str__(self):
        return self.task