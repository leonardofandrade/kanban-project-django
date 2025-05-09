import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kanban_project.settings')

import django
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser created successfully")
    else:
        user = User.objects.get(username='admin')
        user.set_password('admin123')
        user.save()
        print("Superuser password updated successfully")

if __name__ == '__main__':
    create_superuser()
