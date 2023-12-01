# management/commands/create_categories.py
from django.core.management.base import BaseCommand
from uw_app.models import Reminder

class Command(BaseCommand):
    help = 'Create reminders'

    def handle(self, *args, **options):
        reminders = [
            "Maybe your opponent is just having a good day.",
            "Happy winning wargames Wednesday.",
            "Remember to drink water.",
            "Have you meditated today?",
            "Got milk?",
            "Remember to document your projects and progress!",
            "It's okay to fail, learn from it and continue.",
            "Try to really focus when completing a timed task.",
            "Implement your best techniques for memory when retaining information!"
        ]
        
        for single_reminder in reminders:
            # Check if the Category already exists
            existing_reminder, created = Reminder.objects.get_or_create(
                reminder = single_reminder
            )

            # You can update or add on to the existing object if it already exists
            if not created:
                existing_reminder.save()

        self.stdout.write(self.style.SUCCESS('Reminders processed successfully'))