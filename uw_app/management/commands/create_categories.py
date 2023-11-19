# management/commands/create_categories.py
from django.core.management.base import BaseCommand
from uw_app.models import Category

class Command(BaseCommand):
    help = 'Create categories'

    def handle(self, *args, **options):
        categories = ['Creativity', 'Intelligence', 'Essentials', 'Knowledge', 'Games']
        
        for category_name in categories:
            Category.objects.create(name=category_name)

        self.stdout.write(self.style.SUCCESS('Categories created successfully'))
