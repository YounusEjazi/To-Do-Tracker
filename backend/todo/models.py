from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.

class BaseModel(models.Model):  # Inherit from models.Model
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Use = for assignment
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Mark this model as abstract

class Todo(BaseModel):  # Inherit from BaseModel which itself inherits from models.Model
    todo_name = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_todos")

    def __str__(self):
        return self.todo_name
