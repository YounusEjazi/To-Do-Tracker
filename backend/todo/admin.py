# --- admin.py ---
from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = (
        'todo_name', 'user', 'priority', 'is_completed', 'due_date',
        'is_pinned', 'completed_at'
    )
    list_filter = ('priority', 'is_completed', 'is_pinned', 'due_date')
    search_fields = ('todo_name', 'user__username')
    ordering = ('-is_pinned', 'due_date')
