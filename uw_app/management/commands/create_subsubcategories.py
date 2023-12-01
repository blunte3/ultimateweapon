# management/commands/create_subsubcategories.py
from django.core.management.base import BaseCommand
from uw_app.models import Category, Subcategory, Subsubcategory

class Command(BaseCommand):
    help = 'Create subsubcategories'

    def handle(self, *args, **options):
        categories = Category.objects.all()

        subsubcategories_per_subcategory = {
            'Instruments': ['Kalimba', 'Drums', 'Guitar', 'Piano', 'Ukulele', 'Saxophone'],
            'Art': ['Painting', 'Sculpture', 'Drawing', 'Knitting', 'Sewing'],
            'Writing': ['Stories', 'Journaling', 'Poetry', 'Essays'],
            'Digital': ['Graphic Design', 'Web Development', 'Animation', 'Videos', 'Photography'],
            'Voice': ['Singing', 'Impressions' 'Voice Acting', 'Beatboxing', 'Freestyling'],
            'Musical-Rhythmic': ['Music Theory', 'Perfect Pitch', 'Music Production'],
            'Visual-Spatial': ['Spatial Reasoning', 'Visualization', 'Map Reading'],
            'Linguistic-Verbal': ['Foreign Language', 'Vocab', 'Reading', 'Argument/Debate', 'Presentation/Public Speaking'],
            'Logical-Mathematical': ['Logic', 'Mathematics', 'Problem Solving', 'IQ'],
            'Bodily-Kinesthetic': ['Dancing', 'Calisthenics', 'Bodily Control'],
            'Interpersonal': ['Communication', 'Teamwork', 'Leadership', 'Active Listening', 'Human Response'],
            'Intrapersonal': ['Self-awareness', 'Self-reflection', 'Psychology','Meditation'],
            'Existential': ['Spirituality', 'Politics'],
            'Naturalist': ['Observation', 'Exploration', 'Classification'],
            'Kitchen': ['Cooking Knowledge', 'Meals', 'Dishes', 'Cutting/Preparing'],
            'Cleaning': ['Home Cleaning', 'Organization', 'Product Knowledge'],
            'Handy-Man': ['Woodworking', 'Plumbing', 'Electrical', 'Welding', 'Mechanic', 'Manual Driving'],
            'Money': ['Budgeting', 'Selling', 'Trading', 'Investing'],
            'Fighting': ['Self-Defense', 'Martial Arts', 'Striking', 'Grappling', 'Weapons'],
            'Survival': ['Outdoor Survival', 'First Aid', 'Wilderness Skills', 'Resourcefulness'],
            'History': ['Space History', 'Ancient History', 'Modern History'],
            'Science': ['Physics', 'Biology', 'Chemistry', 'Anatomy', 'Earth Science'],
            'Technology': ['Computers', 'Electrical Engineering', 'Programming', 'Mechanical Engineering'],
            'Random': ['Trivia / Random Facts'],
            'Philosophy': ['Ethics', 'Metaphysics', 'Religion', 'Epistemology'],
            'Video': ['Fighting', 'Party', 'Platformer', 'FPS'],
            'Barbecue': ['Cornhole', 'Ladderball', 'Die'],
            'Board': ['Monopoly', 'Catan', 'Coup', 'Chess', 'Divinum'],
            'Sports': ['Soccer', 'Basketball', 'Tennis', 'Gymnastics', 'Skating'],
            'Security / Hacking': ['Cybersecurity', 'Hacking', 'Lockpicking'],
            'Reconnaissance': ['Surveillance/Information Gathering', 'Analysis'],
            'Parkour': ['Techniques', 'Climbing', 'Obstacle Course'],
            'Cognitive Function': ['Working Memory', 'Attention', 'Executive Function', 'Short Term Memory'],
            'Emotional Function': ['Sadness', 'Happiness', 'Fear', 'Anger', 'Surprise', 'Disgust'],
            'Motor Function': ['Running/Sprinting', 'Jumping', 'Balancing', 'Coordination'],
            # Add more subcategories and subsubcategories as needed
        }

        for category in categories:
            subcategories = Subcategory.objects.filter(category=category)

            for subcategory in subcategories:
                subsubcategories = subsubcategories_per_subcategory.get(subcategory.name, [])

                for subsubcategory_name in subsubcategories:
                    Subsubcategory.objects.create(name=subsubcategory_name, subcategory=subcategory)

                self.stdout.write(self.style.SUCCESS(f'Subsubcategories created successfully for {subcategory.name}'))
