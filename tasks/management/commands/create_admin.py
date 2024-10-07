from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@gmail.com', 'password')
            self.stdout.write(self.style.SUCCESS('===================>Superuser succesfully created.<==================='))
        else:
            self.stdout.write(self.style.SUCCESS('===================>Superuser already exists.<==================='))