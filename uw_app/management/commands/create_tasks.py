from django.core.management.base import BaseCommand
from uw_app.models import Task, Subcategory

class Command(BaseCommand):
    help = 'Create tasks for all users'

    def handle(self, *args, **options):
        subcategories = Subcategory.objects.all()

        # Define tasks for each subcategory with XP points
        tasks_per_subcategory = {
            'Music': [('Sing a full song and analyze', 5, 'daily'), ('Play instrument for 20 min', 5, 'daily'), ('Make music', 5, 'daily'), ('Perfect singing a song', 10, 'weekly'), ('Learn a song on an instrument', 10, 'weekly'), ('Make and perform a song', 20, 'monthly'), ('Perform a song on an instrument', 20, 'monthly')],
            'Art': [('Paint for 20 min', 5, 'daily'), ('Sculpt for 20 min', 5, 'daily'), ('Draw for 20 min', 5, 'daily'), ('Sew for 30 min', 8, 'daily'), ('Complete a painting', 10, 'weekly'), ('Complete a sculpture', 12, 'weekly'), ('Complete a drawing', 11, 'weekly'), ('Finish a sewing project', 15, 'weekly'), ('Make a painting portfolio', 30, 'monthly'), ('Make a sculpture portfolio', 30, 'monthly'), ('Make a drawing portfolio', 30, 'monthly'), ('Make a sewing portfolio', 30, 'monthly')],
            'Writing': [('Write a story', 5, 'daily'), ('Journal thoughts', 3, 'daily'), ('Write an essay', 10, 'weekly'), ('Write a chapter in a book', 13, 'weekly'), ('Write about your day in depth', 6, 'daily'), ('Write a book', 50, 'monthly')],
            'Digital': [('Make a presentation', 10, 'weekly'), ('Record video', 5, 'daily'), ('Photograph', 5, 'daily'), ('Come up with an animation', 3, 'daily'), ('Present a presentation', 10, 'weekly'), ('Edit a video', 10, 'weekly'), ('Edit photographs', 10, 'weekly'), ('Create an animation', 15, 'weekly'), ('Create and give a ted talk', 20, 'monthly'), ('Finalize a video and share', 20, 'monthly'), ('Finalize photographs and share', 20, 'monthly'), ('Finalize animation and share', 20, 'monthly')],
            'Musical-Rhythmic': [('Study music theory 20 min', 5, 'daily'), ('Perfect pitch training 20 min', 5, 'daily'), ('Produce music', 8, 'daily'), ('Practice music theory', 9, 'daily'), ('Perfect pitch training for 30 min', 8, 'daily'), ('Produce a full song', 13, 'weekly'), ('Demonstrate perfect pitch', 30, 'monthly'), ('Demonstrate music theory', 20, 'monthly')],
            'Visual-Spatial': [('Visualization training', 5, 'daily'), ('Spatial training', 5, 'daily'), ('Visual-Spatial training for 30 min', 10, 'weekly')],
            'Linguistic-Verbal': [('Study vocab for 10 min', 3, 'daily'), ('Read for 20 min', 5, 'daily'), ('Practice argument and debate for 20 min', 5, 'daily'), ('Recite learned vocab and learn', 10, 'weekly'), ('Read for 60 min', 10, 'weekly'), ('Demonstrate use of retained vocab', 30, 'monthly'), ('Read an entire book with notes', 40, 'monthly')],
            'Logical-Mathematical': [('Argument map for 20 min', 5, 'daily'), ('Brainteasers for 20 min', 5, 'daily'), ('Logic puzzles for 20 min', 5, 'daily'), ('N-back for 20 min', 5, 'daily'), ('Corsi block for 20 min', 5, 'daily'), ('Practice debate with a person', 10, 'weekly'), ('Argument map for 30 min', 7, 'daily'), ('Mensa/IQ test training', 10, 'weekly'), ('N-back training for 20 min', 10, 'weekly'), ('Pass Mensa IQ test', 40, 'monthly')],
            'Bodily-Kinesthetic': [('Practice dancing for 20 min', 5, 'daily'), ('Calisthenics for 20 min', 5, 'daily'), ('Cold therapy for 10 min', 5, 'daily'), ('Learn a dance', 10, 'weekly'), ('Learn a new calisthenic move', 14, 'weekly'), ('Cold therapy withour shivering 10 min', 10, 'weekly'), ('Learn and perform a dance', 30, 'monthly'), ('Learn a more impressive calisthenic move', 20, 'monthly'), ('Climb a mountain in shorts', 30, 'monthly')],
            'Interpersonal': [('Talk to someone new', 3, 'daily'), ('Practice empathy', 4, 'daily'), ('Active listening', 5, 'daily'), ('Human response research for 20 min', 5, 'daily'), ('Make a new friend', 10, 'weekly'), ('Have an in depth conversation', 10, 'weekly'), ('Understand and analyze how people work', 20, 'monthly')],
            'Intrapersonal': [('Self reflection for 10 min', 4, 'daily'), ('Meditation for 20 min', 5, 'daily'), ('Journaling for 10 min', 5, 'daily'), ('Journal about the previous weeks', 20, 'monthly')],
            'Existential': [('Form philosophical thoughts for 20 min', 5, 'daily'), ('Meditation for 10 min', 3, 'daily'), ('Meditate for 30 min', 10, 'weekly'), ('Form political and philosophical opinions', 20, 'monthly')],
            'Naturalist': [('Take a walk in nature', 5, 'daily'), ('Observe and record the area', 2, 'daily'), ('Classify something you see', 2, 'daily'), ('Go on a hike', 10, 'weekly'), ('Classify and record samples in nature', 10, 'weekly'), ('Climb a mountain', 20, 'monthly'), ('Seek out and analyze something in nature', 20, 'monthly')],
            'Cooking': [('Learn about cooking for 10 min', 3, 'daily'), ('Do the dishes', 4, 'daily'), ('Cook a nice meal', 10, 'weekly'), ('Cook a full meal and get it reviewed', 25, 'monthly')],
            'Cleaning': [('Learn about cleaning for 10 min', 3, 'daily'), ('Sweep the floor', 4, 'daily'), ('Clean the bathrooms', 8, 'daily'), ('Clean for 10 min', 5, 'daily'), ('Deep clean for 30 min', 10, 'weekly'), ('Deep clean a whole area and change something in the room', 30, 'monthly'), ('Invent new cleaning supplies', 25, 'monthly')],
            'Fixing': [('Research woodworking for 10 min', 4, 'daily'), ('Research plumbing for 10 min', 4, 'daily'), ('Research electrical for 10 min', 4, 'daily'), ('Research welding for 10 min', 4, 'daily'), ('Make a woodworking project', 12, 'weekly'), ('Work on plumbing', 10, 'weekly'), ('Work on welding', 10, 'weekly'), ('Work on electrical', 10, 'weekly'), ('Learn to build a house', 40, 'monthly')],
            'Fighting': [('Work on striking for 15 min', 6, 'daily'), ('Work on grappling for 15 min', 6, 'daily'), ('Work on weapons for 10 min', 3, 'daily'), ('Spar someone', 10, 'weekly')],
            'Survival': [('Learn first aid for 10 min', 4, 'daily'), ('Research survival for 10 min', 3, 'daily'), ('Start a fire', 10, 'weekly'), ('Start a fire without lighters', 30, 'monthly')],
            'History': [('Learn ancient history for 10 min', 3, 'daily'), ('Learn about modern history for 10 min', 4, 'daily'), ('Learn about ancient history for 20 min', 10, 'weekly'), ('Learn about modern history for 20 min', 10, 'weekly'), ('Make a report on something in history', 25, 'monthly')],
            'Science': [('Learn something new in physics', 2, 'daily'), ('Learn something new in chemistry', 2, 'daily'), ('Learn something new in computers', 2, 'daily'), ('Learn something new in engineering', 2, 'daily'), ('Make a report on something in science', 25, 'monthly')],
            'Random': [('Learn a random fact', 2, 'daily'), ('Learn something new in depth', 10, 'weekly'), ('Make a report on something new', 25, 'monthly')],
            'Philosophy': [('Read philosophy for 20 min', 5, 'daily'), ('Discover new philosophical ideal', 3, 'daily'),('Make a report on something in philosophy', 25, 'monthly')],
            'Video': [('Play smash', 2, 'daily'), ('Play mario kart', 2, 'daily'), ('Play valorant', 2, 'daily'), ('Play fortnite', 2, 'daily'), ('Win a video game', 10, 'weekly'),('Play in a game tournament', 20, 'monthly')],
            'Barbecue': [('Play cornhole', 3, 'daily'), ('Play ladderball', 3, 'daily'), ('Play frisbee golf', 5, 'daily'), ('Win a barbecue game', 10, 'weekly')],
            'Board': [('Play monopoly', 2, 'daily'), ('Play catan', 3, 'daily'), ('Play coup', 2, 'daily'), ('Win board game', 10, 'weekly')],
            'Sports': [('Play soccer', 5, 'daily'), ('Play basketball', 5, 'daily'), ('Go rockclimbing', 10, 'weekly'), ('Play table tennis', 10, 'weekly'), ('Win at a sport', 10, 'weekly')],
            'WorkingMemory': [('N-back for 10 min', 3, 'daily'), ('Complex working memory for 10 min', 3, 'daily')],
            'ExecutiveFunction': [('Executive function training for 10 min', 3, 'daily')],
            'Memory': [('Try to remember something very detailed', 2, 'daily'), ('Memorize digits of pi', 5, 'daily')],
            # Add more subcategories and tasks with XP points as needed
        }

        for subcategory in subcategories:
            tasks = tasks_per_subcategory.get(subcategory.name, [])

            for task_name, xp, type in tasks:
                Task.objects.create(name=task_name, subcategory=subcategory, xp=xp, type=type)

            self.stdout.write(self.style.SUCCESS(f'Tasks created successfully for {subcategory.name}'))