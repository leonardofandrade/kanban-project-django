from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from django.core.serializers.json import DjangoJSONEncoder
import json
from .models import Project, Column, Task

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'kanban/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Tasks by status
        status_counts = Task.objects.values('status').annotate(count=Count('id'))
        context['status_counts'] = json.dumps(list(status_counts), cls=DjangoJSONEncoder)
        
        # Tasks by priority/label
        label_counts = Task.objects.values('label').annotate(count=Count('id'))
        context['label_counts'] = json.dumps(list(label_counts), cls=DjangoJSONEncoder)
        
        # Tasks by assignee
        assignee_counts = Task.objects.exclude(assigned_to=None)\
            .values('assigned_to__username')\
            .annotate(count=Count('id'))
        context['assignee_counts'] = json.dumps(list(assignee_counts), cls=DjangoJSONEncoder)
        
        # Project completion stats
        projects = Project.objects.all()
        project_stats = []
        for project in projects:
            total_tasks = Task.objects.filter(column__project=project).count()
            completed_tasks = Task.objects.filter(
                column__project=project,
                status='done'
            ).count()
            if total_tasks > 0:
                completion = (completed_tasks / total_tasks) * 100
            else:
                completion = 0
            project_stats.append({
                'name': project.title,
                'completion': completion
            })
        context['project_stats'] = json.dumps(project_stats, cls=DjangoJSONEncoder)
        
        # Tasks due soon (next 7 days)
        today = timezone.now().date()
        week_later = today + timedelta(days=7)
        upcoming_tasks = Task.objects.filter(
            due_date__range=[today, week_later]
        ).order_by('due_date')
        context['upcoming_tasks'] = upcoming_tasks
        
        return context
