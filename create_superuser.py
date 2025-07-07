from django.contrib.auth.models import User
from django.core.management import setup_environ
from config import settings

setup_environ(settings)

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser created successfully")
else:
    print("Superuser already exists")
