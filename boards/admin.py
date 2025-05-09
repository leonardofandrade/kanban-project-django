from django.contrib import admin
from .models import Project, Column, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')
    list_filter = ('created_at', 'owner')
    search_fields = ('title', 'description')
    filter_horizontal = ('members',)

@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'order')
    list_filter = ('project',)
    search_fields = ('title', 'project__title')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'column', 'created_by', 'assigned_to', 'due_date', 'label')
    list_filter = ('created_at', 'due_date', 'label', 'column__project')
    search_fields = ('title', 'description', 'created_by__username', 'assigned_to__username')
    raw_id_fields = ('created_by', 'assigned_to')
