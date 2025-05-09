from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from boards.models import Project, Column, Task
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Create test data: 3 projects, users, columns, and 30 tasks'

    def handle(self, *args, **options):
        # Create users
        users_data = [
            {'username': 'alice', 'email': 'alice@example.com'},
            {'username': 'bob', 'email': 'bob@example.com'},
            {'username': 'carol', 'email': 'carol@example.com'},
        ]
        users = []
        for udata in users_data:
            user, created = User.objects.get_or_create(username=udata['username'], defaults={'email': udata['email']})
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))

        # Create projects
        projects = []
        owner = User.objects.filter(is_superuser=True).first() or users[0]
        for i in range(1, 4):
            project, created = Project.objects.get_or_create(
                title=f'Project {i}',
                defaults={'description': f'Description for project {i}', 'owner': owner}
            )
            projects.append(project)
        self.stdout.write(self.style.SUCCESS(f'Created {len(projects)} projects'))

        # Create columns for each project
        column_titles = ['To Do', 'In Progress', 'Done']
        for project in projects:
            for title in column_titles:
                Column.objects.get_or_create(project=project, title=title)
        self.stdout.write(self.style.SUCCESS('Created columns for each project'))

        # Create tasks
        labels = ['low', 'medium', 'high']
        statuses = ['todo', 'in_progress', 'done']
        all_columns = Column.objects.all()
        tasks_created = 0
        created_by = User.objects.filter(is_superuser=True).first() or users[0]
        for i in range(1, 31):
            project = random.choice(projects)
            column = random.choice(all_columns.filter(project=project))
            assigned_to = random.choice(users)
            task = Task.objects.create(
                title=f'Task {i}',
                description=f'Description for task {i}',
                assigned_to=assigned_to,
                due_date=timezone.now().date(),
                label=random.choice(labels),
                status=random.choice(statuses),
                column=column,
                order=0,
                created_by=created_by,
            )
            tasks_created += 1
        self.stdout.write(self.style.SUCCESS(f'Created {tasks_created} tasks'))
