# management/commands/create_subcategories.py
from django.core.management.base import BaseCommand
from uw_app.models import Category, Subcategory

class Command(BaseCommand):
    help = 'Create subcategories'

    def handle(self, *args, **options):
        categories = Category.objects.all()

        subcategories_per_category = {
            'Creativity': ['Music', 'Art', 'Writing', 'Digital'],
            'Intelligence': ['Musical-Rhythmic', 'Visual-Spatial', 'Linguistic-Verbal', 'Logical-Mathematical', 'Bodily-Kinesthetic', 'Interpersonal', 'Intrapersonal', 'Existential', 'Naturalist'],
            'Essentials': ['Cooking', 'Cleaning', 'Fixing', 'Fighting', 'Survival'],
            'Knowledge': ['History', 'Science', 'Random', 'Philosophy'],
            'Games': ['Video', 'Barbecue', 'Board', 'Sports'],
            'Cognition': ['WorkingMemory', 'ExecutiveFunction','Memory'],
            # Add more categories and subcategories as needed
        }

        for category in categories:
            subcategories = subcategories_per_category.get(category.name, [])

            for subcategory_name in subcategories:
                Subcategory.objects.create(name=subcategory_name, category=category)

            self.stdout.write(self.style.SUCCESS(f'Subcategories created successfully for {category.name}'))
