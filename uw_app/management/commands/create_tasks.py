from django.core.management.base import BaseCommand
from uw_app.models import Task, Subcategory

class Command(BaseCommand):
    help = 'Create tasks for all users'

    def handle(self, *args, **options):
        subcategories = Subcategory.objects.all()

        # Define tasks for each subcategory with XP points
        tasks_per_subcategory = {
            'Music': [('Sing a full song and analyze', 5), ('Play instrument for 20 min', 5), ('Make music', 5), ('Perfect singing a song', 10), ('Learn a song on an instrument', 10), ('Make and perform a song', 20), ('Perform a song on an instrument', 20)],
            'Art': [('Paint for 20 min', 5), ('Sculpt for 20 min', 5), ('Draw for 20 min', 5), ('Sew for 30 min', 8), ('Complete a painting', 10), ('Complete a sculpture', 12), ('Complete a drawing', 11), ('Finish a sewing project', 15), ('Make a painting portfolio', 30), ('Make a sculpture portfolio', 30), ('Make a drawing portfolio', 30), ('Make a sewing portfolio', 10)],
            'Writing': [('Write a story', 5), ('Journal thoughts', 3), ('Write an essay', 10), ('Write a chapter in a book', 13), ('Write about your day in depth', 6), ('Write a book', 50)],
            'Digital': [('Make a presentation', 10), ('Record video', 5), ('Photograph', 5), ('Come up with an animation', 3), ('Present a presentation', 10), ('Edit a video', 10), ('Edit photographs', 10), ('Create an animation', 15), ('Create and give a ted talk', 20), ('Finalize a video and share', 20), ('Finalize photographs and share', 20), ('Finalize animation and share', 20)],
            'Musical-Rhythmic': [('Study music theory 20 min', 5), ('Perfect pitch training 20 min', 5), ('Produce music', 8), ('Practice music theory', 9), ('Perfect pitch training for 30 min', 8), ('Produce a full song', 13), ('Demonstrate perfect pitch', 30), ('Demonstrate music theory', 20)],
            'Visual-Spatial': [('Visualization training', 5), ('Spatial training', 5), ('Visual-Spatial training for 30 min', 10)],
            'Linguistic-Verbal': [('Study vocab for 10 min', 3), ('Read for 20 min', 5), ('Practice argument and debate for 20 min', 5), ('Recite learned vocab and learn', 10), ('Read for 60 min', 10), ('Demonstrate use of retained vocab', 30), ('Read an entire book with notes', 40)],
            'Logical-Mathematical': [('Argument map for 20 min', 5), ('Brainteasers for 20 min', 5), ('Logic puzzles for 20 min', 5), ('N-back for 20 min', 5), ('Corsi block for 20 min', 5), ('Practice debate with a person', 10), ('Argument map for 30 min', 7), ('Mensa/IQ test training', 10), ('N-back training for 20 min', 10), ('Pass Mensa IQ test', 40)],
            'Bodily-Kinesthetic': [('Practice dancing for 20 min', 5), ('Calisthenics for 20 min', 5), ('Cold therapy for 10 min', 5), ('Learn a dance', 10), ('Learn a new calisthenic move', 14), ('Cold therapy withour shivering 10 min', 10), ('Learn and perform a dance', 30), ('Learn a more impressive calisthenic move', 20), ('Climb a mountain in shorts', 30)],
            'Interpersonal': [('Talk to someone new', 3), ('Practice empathy', 4), ('Active listening', 5), ('Human response research for 20 min', 5), ('Make a new friend', 10), ('Have an in depth conversation', 10), ('Understand and analyze how people work', 20)],
            'Intrapersonal': [('Self reflection for 10 min', 4), ('Meditation for 20 min', 5), ('Journaling for 10 min', 5), ('Journal about the previous weeks', 20)],
            'Existential': [('Form philosophical thoughts for 20 min', 5), ('Meditation for 10 min', 3), ('Meditate for 30 min', 10), ('Form political and philosophicla opinions', 20)],
            'Naturalist': [('Take a walk in nature', 5), ('Observe and record the area', 2), ('Classify something you see', 2), ('Go on a hike', 10), ('Classify and record samples in nature', 10), ('Climb a mountain', 20), ('Seek out and analyze something in nature', 20)],
            'Cooking': [('Learn about cooking for 10 min', 3), ('Do the dishes', 4), ('Cook a nice meal', 10), ('Cook a full meal and get it reviewed', 25)],
            'Cleaning': [('Learn about cleaning for 10 min', 3), ('Sweep the floor', 4), ('Clean the bathrooms', 8), ('Clean for 10 min', 5), ('Deep clean for 30 min', 10), ('Deep clean a whole area and change something in the room', 30), ('Invent new cleaning supplies', 25)],
            'Fixing': [('Research woodworking for 10 min', 4), ('Research plumbing for 10 min', 4), ('Research electrical for 10 min', 4), ('Research welding for 10 min', 4), ('Make a woodworking project', 12), ('Work on plumbing', 10), ('Work on welding', 10), ('Work on electrical', 10), ('Learn to build a house', 40)],
            'Fighting': [('Work on striking for 15 min', 6), ('Work on grappling for 15 min', 6), ('Work on weapons for 10 min', 3), ('Spar someone', 10)],
            'Survival': [('Learn first aid for 10 min', 4), ('Research survival for 10 min', 3), ('Start a fire', 10), ('Start a fire without lighters', 30)],
            'History': [('Learn ancient history for 10 min', 3), ('Learn about modern history for 10 min', 4), ('Learn about ancient history for 20 min', 10), ('Learn about modern history for 20 min', 10), ('Make a report on something in history', 25)],
            'Science': [('Learn something new in physics', 2), ('Learn something new in chemistry', 2), ('Learn something new in computers', 2), ('Learn something new in engineering', 2), ('Make a report on something in science', 25)],
            'Random': [('Learn a random fact', 2), ('Learn something new in depth', 10), ('Make a report on something new', 25)],
            'Philosophy': [('Read philosophy for 20 min', 5), ('Discover new philosophical ideal', 3),('Make a report on something in philosophy', 25)],
            'Video': [('Play smash', 2), ('Play mario kart', 2), ('Play valorant', 2), ('Play fortnite', 2), ('Win a video game', 10),('Play in a game tournament', 20)],
            'Barbecue': [('Play cornhole', 3), ('Play ladderball', 3), ('Play frisbee golf', 5), ('Win a barbecue game', 10)],
            'Board': [('Play monopoly', 2), ('Play catan', 3), ('Play coup', 2), ('Win board game', 10)],
            'Sports': [('Play soccer', 5), ('Play basketball', 5), ('Go rockclimbing', 10), ('Play table tennis', 10), ('Win at a sport', 10)],
            'WorkingMemory': [('N-back for 10 min', 3), ('Complex working memory for 10 min', 3)],
            'ExecutiveFunction': [('Executive function training for 10 min', 3)],
            'Memory': [('Try to remember something very detailed', 2), ('Memorize digits of pi', 5)],
            # Add more subcategories and tasks with XP points as needed
        }

        for subcategory in subcategories:
            tasks = tasks_per_subcategory.get(subcategory.name, [])

            for task_name, xp in tasks:
                Task.objects.create(name=task_name, subcategory=subcategory, xp=xp)

            self.stdout.write(self.style.SUCCESS(f'Tasks created successfully for {subcategory.name}'))