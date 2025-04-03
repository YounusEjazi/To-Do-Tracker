# --- serializers.py ---
from rest_framework import serializers
from .models import Todo, SubTask, Comment, Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color']

class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'name', 'is_completed']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']

class TodoSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    assignees = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Todo
        fields = [
            'uuid', 'todo_name', 'description', 'is_completed', 'completed_at',
            'due_date', 'priority', 'is_pinned', 'attachment', 'repeat',
            'tags', 'assignees', 'user', 'subtasks', 'comments'
        ]
        read_only_fields = ['uuid', 'completed_at', 'user']
