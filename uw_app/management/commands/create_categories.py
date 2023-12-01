# management/commands/create_categories.py
from django.core.management.base import BaseCommand
from uw_app.models import Category

class Command(BaseCommand):
    help = 'Create categories'

    def handle(self, *args, **options):
        categories = ['Creativity', 'Intelligence', 'Essentials', 'Knowledge', 'Games', 'Secret Agent', 'Brain']
        
        for category_name in categories:
            # Check if the Category already exists
            existing_category, created = Category.objects.get_or_create(
                name=category_name
            )

            # You can update or add on to the existing object if it already exists
            if not created:
                existing_category.save()

        self.stdout.write(self.style.SUCCESS('Categories processed successfully'))