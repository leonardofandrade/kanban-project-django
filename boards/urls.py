from django.urls import path
from . import views
from .dashboard_views import DashboardView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', views.ProjectListView.as_view(), name='project-list'),
    path('project/new/', views.ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),
    
    # Column URLs
    path('project/<int:project_id>/column/create/', views.create_column, name='column-create'),
    
    # Task URLs
    path('column/<int:column_id>/task/create/', views.create_task, name='task-create'),
    path('task/<int:task_id>/update/', views.update_task, name='task-update'),
    path('task/<int:task_id>/delete/', views.delete_task, name='task-delete'),
    path('task/<int:task_id>/move/', views.move_task, name='task-move'),

    # New tabular task views
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('task/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task-edit'),
]
