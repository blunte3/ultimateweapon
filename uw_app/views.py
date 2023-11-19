from django.shortcuts import redirect, render
from django.core.cache import cache
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from uw_app.models import CustomUser, Task, Subcategory, Category
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from uw_project import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from random import shuffle
import random
from datetime import timedelta
from django.utils import timezone
from email.message import EmailMessage
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
def home(request):
    return render(request, "uw_app/index.html")

def signup(request):

    if request.method == "POST":
        # username = request.POST.get('username')
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exists! Please try again.")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('home')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters.")

        if pass1 != pass2:
            messages.error(request, "Password did not match!")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('home')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.user_name = username
        myuser.is_active = False
        myuser.save()

        messages.success(request, "Your Account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account.")

        # Welcome Email

        subject = "Welcome to Ultimate Weapon!"
        message = "Hello " + myuser.user_name + "!! \n" + "Welcome to Ultimate Weapon! \n Thank you for visiting the website \n We have also sent you a confirmation email, please confirm your email address in order to activate your account. \n\n Thanking you\n Evan Blunt"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


        # Email Address Confirmation Email

        current_site = get_current_site(request)
        email_subject = "Confirm your email @ Ultimate Weapon - Django Login!"
        message2 = render_to_string('uw_app/email_confirmation.html', {
            'name': myuser.user_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')

    return render(request, "uw_app/signup.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            return render(request, "uw_app/index.html", {'username': username})

        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')

    return render(request, "uw_app/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!")
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect('home')
    else:
        return render(request, 'uw_app/activation_failed.html')
    
def index(request):
    user = request.user
    custom_user, created = CustomUser.objects.get_or_create(user=user)
    print(custom_user.display_name, custom_user.character_image, custom_user.difficulty)

    if request.method == 'POST':
        # Handle form submission (either signup form or settings form)
        character_image = request.POST.get('character_image')
        display_name = request.POST.get('display_name')
        difficulty = request.POST.get('difficulty')

        # Update or create CustomUser instance for the current user
        custom_user, created = CustomUser.objects.get_or_create(user=user)
        custom_user.character_image = character_image
        custom_user.display_name = display_name
        custom_user.difficulty = difficulty
        custom_user.save()

        return redirect('index')  # Redirect to the index page after form submission

    # Fetch CustomUser instance for the current user
    custom_user, created = CustomUser.objects.get_or_create(user=user)

    return render(request, 'uw_app/index.html', {
        'display_name': custom_user.display_name,
        'character_image': custom_user.character_image,
        'difficulty': custom_user.difficulty,
    })


@login_required
def settings(request):
    if request.user.is_authenticated:
        custom_user, created = CustomUser.objects.get_or_create(user=request.user)
        
        if request.method == 'POST':
            character_image = request.POST.get('character_image')
            display_name = request.POST.get('display_name')
            difficulty = request.POST.get('difficulty')
            pathway = request.POST.get('pathway')

            # Update the CustomUser object with the new data
            custom_user.character_image = character_image
            custom_user.display_name = display_name
            custom_user.difficulty = difficulty
            custom_user.pathway = pathway
            custom_user.save()

            return redirect('settings')  # Redirect to settings page after saving changes
        else:
            # If it's a GET request, populate the form with existing data
            character_image = custom_user.character_image
            display_name = custom_user.display_name
            difficulty = custom_user.difficulty
            pathway = custom_user.pathway

        return render(request, 'uw_app/settings.html', {
            'character_image': character_image,
            'display_name': display_name,
            'difficulty': difficulty,
            'pathway': pathway,
        })
    else:
        return redirect('home')
    

class TaskEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Task):
            return {
                'id': obj.id,
                'name': obj.name,
                'xp': obj.xp,
                'completed': obj.completed,
                'subcategory': obj.subcategory.id,  # Assuming you want to include the subcategory ID
                # Include other fields as needed
            }
        return super().default(obj)
    
@login_required
def player(request):
    print('Player view is being called.')
    if request.user.is_authenticated:
        # Define a unique cache key for the user's tasks
        cache_key = f'user_tasks_{request.user.id}'
        custom_user, created = CustomUser.objects.get_or_create(user=request.user)
        # Get the authenticated user's pathway and difficulty level
        user_pathway = custom_user.pathway
        user_difficulty = custom_user.difficulty
        # Try to get the tasks from the cache
        short_tasks = custom_user.short_tasks
        medium_tasks = custom_user.medium_tasks
        long_tasks = custom_user.long_tasks
        


        if not short_tasks and medium_tasks and long_tasks: 
            if user_pathway == 'SCHOLAR':
                category_names = ['Creativity', 'Intelligence', 'Knowledge']
            elif user_pathway == 'TINKERER':
                category_names = ['Essentials', 'Games', 'Intelligence']
            elif user_pathway == 'CREATIVE':
                category_names = ['Creativity', 'Knowledge', 'Games']
            else:
                category_names = Category.objects.values_list('name', flat=True)

            tasks = Task.objects.filter(subcategory__category__name__in=category_names, completed=False)

            # Categorize tasks based on XP points
            short_tasks = []
            medium_tasks = []
            long_tasks = []

            for task in tasks:
                if task.xp < 10:
                    short_tasks.append(task)
                elif task.xp < 20:
                    medium_tasks.append(task)
                else:
                    long_tasks.append(task)

            random.shuffle(short_tasks)
            random.shuffle(medium_tasks)
            random.shuffle(long_tasks)

            # Select the appropriate number of tasks based on the difficulty level
            if user_difficulty == "Easy":
                current_short = short_tasks[:2]
                current_medium = medium_tasks[:1]                    
                current_long = long_tasks[:1]
            elif user_difficulty == "Medium":
                current_short = short_tasks[:3]
                current_medium = medium_tasks[:2]
                current_long = long_tasks[:1]
            elif user_difficulty == "Hard":
                current_short = short_tasks[:4]
                current_medium = medium_tasks[:3]
                current_long = long_tasks[:1]
            elif user_difficulty == "Ultimate Weapon":
                current_short = short_tasks[:5]
                current_medium = medium_tasks[:3]
                current_long = long_tasks[:2]

            short_tasks = current_short
            medium_tasks = current_medium
            long_tasks = current_long
                
            # When updating tasks
            custom_user.short_tasks = [task.id for task in short_tasks]
            custom_user.medium_tasks = [task.id for task in medium_tasks]
            custom_user.long_tasks = [task.id for task in long_tasks]
            custom_user.save()

        short_task_ids = custom_user.short_tasks
        medium_task_ids = custom_user.medium_tasks
        long_task_ids = custom_user.long_tasks

        short_tasks = Task.objects.filter(id__in=short_task_ids)
        medium_tasks = Task.objects.filter(id__in=medium_task_ids)
        long_tasks = Task.objects.filter(id__in=long_task_ids)



        return render(request, 'uw_app/player.html', {
            'display_name': custom_user.display_name,
            'character_image': custom_user.character_image,
            'difficulty': custom_user.difficulty,
            'pathway': custom_user.pathway,
            'total_xp': custom_user.total_xp,
            'short_tasks': short_tasks,
            'medium_tasks': medium_tasks,
            'long_tasks': long_tasks,
        })
    else:
        # Redirect to the home page or display an error message for unauthenticated users
        return redirect('home')


@login_required
def complete_task(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        task_id = request.POST.get('task_id')

        try:
            task = Task.objects.get(id=task_id, completed=False)  # Ensure the task is not already completed
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found or already completed.'})

        # Mark the task as completed
        task.completed = True
        task.save()

        # Update subcategory XP
        subcategory = task.subcategory
        subcategory.xp += task.xp
        subcategory.save()

        # Update category XP
        category = subcategory.category
        category.xp += task.xp
        category.save()

        # Update user's total XP
        custom_user = CustomUser.objects.get(user=request.user)
        custom_user.total_xp += task.xp
        custom_user.save()

        # Check if all tasks in 'Short' are completed
        all_short_tasks_completed = all(Task.objects.get(id=task_id).completed for task_id in custom_user.short_tasks)
        if all_short_tasks_completed:
            # Shuffle and save new tasks
            short_tasks = Task.objects.filter(subcategory__name='Short', completed=False).order_by('?')[:5]
            custom_user.short_tasks = [task.id for task in short_tasks]

        # Check if all tasks in 'Medium' are completed
        all_medium_tasks_completed = all(Task.objects.get(id=task_id).completed for task_id in custom_user.medium_tasks)
        if all_medium_tasks_completed:
            # Shuffle and save new tasks
            medium_tasks = Task.objects.filter(subcategory__name='Medium', completed=False).order_by('?')[:3]
            custom_user.medium_tasks = [task.id for task in medium_tasks]

        # Check if all tasks in 'Long' are completed
        all_long_tasks_completed = all(Task.objects.get(id=task_id).completed for task_id in custom_user.long_tasks)
        if all_long_tasks_completed:
            # Shuffle and save new tasks
            long_tasks = Task.objects.filter(subcategory__name='Long', completed=False).order_by('?')[:2]
            custom_user.long_tasks = [task.id for task in long_tasks]

        custom_user.save()

        print('Complete task view completed.')
        return JsonResponse({'success': True, 'message': 'Task completed successfully.'})
    else:
        print('complete_tasks skipped')
        return JsonResponse({'success': False, 'error': 'Invalid request.'})
