from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Project, Column, Task
from .forms import ProjectForm, ColumnForm, TaskForm, TaskMoveForm
from django.db.models import Q

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'kanban/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return Project.objects.filter(members=self.request.user) | Project.objects.filter(owner=self.request.user)

class ProjectDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Project
    template_name = 'kanban/board.html'
    context_object_name = 'project'

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner or self.request.user in project.members.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['columns'] = self.object.columns.all()
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'kanban/project_form.html'
    success_url = reverse_lazy('project-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        form.instance.members.add(self.request.user)
        
        # Create default columns
        default_columns = ['A Fazer', 'Em Andamento', 'Concluído']
        for i, title in enumerate(default_columns):
            Column.objects.create(
                project=form.instance,
                title=title,
                order=i
            )
        return response

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'kanban/project_form.html'

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'kanban/project_confirm_delete.html'
    success_url = reverse_lazy('project-list')

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner

@login_required
def create_column(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ColumnForm(request.POST)
        if form.is_valid():
            column = form.save(commit=False)
            column.project = project
            column.order = project.columns.count()
            column.save()
            return redirect('project-detail', pk=project.id)
    return redirect('project-detail', pk=project.id)

@login_required
def create_task(request, column_id):
    column = get_object_or_404(Column, id=column_id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.column = column
            task.created_by = request.user
            task.order = column.tasks.count()
            task.save()
    return redirect('project-detail', pk=column.project.id)

@login_required
def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
    return redirect('project-detail', pk=task.column.project.id)

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    project_id = task.column.project.id
    task.delete()
    return redirect('project-detail', pk=project_id)

@login_required
def move_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        form = TaskMoveForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            # Update status based on column title
            column_title = task.column.title.lower()
            if 'fazer' in column_title or 'todo' in column_title:
                task.status = 'todo'
            elif 'andamento' in column_title or 'progress' in column_title:
                task.status = 'in_progress'
            elif 'concluído' in column_title or 'done' in column_title:
                task.status = 'done'
            else:
                task.status = 'todo'
            task.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'kanban/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(assigned_to__username__icontains=query) |
                Q(column__title__icontains=query) |
                Q(status__icontains=query)
            ).distinct()
        return queryset.order_by('status', 'order', 'created_at')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'kanban/task_form.html'

    def get_success_url(self):
        return reverse_lazy('task-list')

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'kanban/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(assigned_to__username__icontains=query) |
                Q(column__title__icontains=query) |
                Q(status__icontains=query)
            ).distinct()
        return queryset.order_by('status', 'order', 'created_at')

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'kanban/task_form.html'

    def get_success_url(self):
        return reverse_lazy('task-list')
