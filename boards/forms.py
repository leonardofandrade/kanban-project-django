from django import forms
from .models import Project, Column, Task

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'members']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'members': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
        }

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'label']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'label': forms.Select(attrs={'class': 'form-select'}),
        }

class TaskMoveForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['column', 'order']
