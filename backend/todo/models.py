# --- models.py ---
from django.db import models
import uuid
from django.contrib.auth.models import User
from django.utils import timezone

class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Tag(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=10)  # e.g. #FF0000

    def __str__(self):
        return self.name

class Todo(BaseModel):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    REPEAT_CHOICES = [
        ('none', 'None'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ]

    todo_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_pinned = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='todo_attachments/', null=True, blank=True)
    repeat = models.CharField(max_length=10, choices=REPEAT_CHOICES, default='none')
    tags = models.ManyToManyField(Tag, blank=True)
    assignees = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_todos")

    def __str__(self):
        return self.todo_name

    @property
    def is_overdue(self):
        return self.due_date and not self.is_completed and self.due_date < timezone.now()

    def save(self, *args, **kwargs):
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.is_completed:
            self.completed_at = None
        super().save(*args, **kwargs)

class SubTask(BaseModel):
    parent = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='subtasks')
    name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Comment(BaseModel):
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.author.username} - {self.text[:30]}"