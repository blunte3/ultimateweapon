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
            selected_subcats = request.POST.getlist('subcategory')
            
            custom_user.pathway.set(selected_subcats)  
            custom_user.save()

            # Update the CustomUser object with the new data
            custom_user.character_image = character_image
            custom_user.display_name = display_name
            custom_user.difficulty = difficulty
            custom_user.save()

            return redirect('settings')  # Redirect to settings page after saving changes
        else:
            # If it's a GET request, populate the form with existing data
            character_image = custom_user.character_image
            display_name = custom_user.display_name
            difficulty = custom_user.difficulty
            pathway = custom_user.pathway
            categories = Category.objects.all()
            subcategories = Subcategory.objects.all()
            selected_subcats = custom_user.pathway.all() 

        return render(request, 'uw_app/settings.html', {
            'character_image': character_image,
            'display_name': display_name,
            'difficulty': difficulty,
            'pathway': pathway,
            'categories': categories,
            'subcategories': subcategories,
            'selected_subcats': selected_subcats,
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
        custom_user, created = CustomUser.objects.get_or_create(user=request.user)

        # Get the authenticated user's pathway and difficulty level
        selected_subcats = custom_user.pathway.all()
        user_difficulty = custom_user.difficulty

        if not custom_user.daily_tasks.exists() and not custom_user.weekly_tasks.exists() and not custom_user.monthly_tasks.exists():
            # Get the ids of those subcategories
            subcat_ids = [subcat.id for subcat in selected_subcats]

            # Filter tasks to only those matching selected subcats 
            tasks = Task.objects.filter(subcategory__in=subcat_ids, completed=False)

            # Categorize tasks based on XP points
            daily_tasks = []
            weekly_tasks = []
            monthly_tasks = []
            current_daily = []
            current_weekly = []
            current_monthly = []
            for task in tasks:
                if task.xp < 10:
                    task.type = "daily"
                    daily_tasks.append(task)
                elif task.xp < 20:
                    task.type = "weekly"
                    weekly_tasks.append(task)
                else:
                    task.type = "monthly"
                    monthly_tasks.append(task)

            shuffle(daily_tasks)
            shuffle(weekly_tasks)
            shuffle(monthly_tasks)

            # Select the appropriate number of tasks based on the difficulty level
            if user_difficulty == "Easy":
                current_daily = daily_tasks[:2]
                current_weekly = weekly_tasks[:1]
                current_monthly = monthly_tasks[:1]
            elif user_difficulty == "Medium":
                current_daily = daily_tasks[:3]
                current_weekly = weekly_tasks[:2]
                current_monthly = monthly_tasks[:1]
            elif user_difficulty == "Hard":
                current_daily = daily_tasks[:4]
                current_weekly = weekly_tasks[:3]
                current_monthly = monthly_tasks[:1]
            elif user_difficulty == "ULTIMATE WEAPON":
                current_daily = daily_tasks[:5]
                current_weekly = weekly_tasks[:3]
                current_monthly = monthly_tasks[:2]

            # When updating tasks
            custom_user.daily_tasks.set(current_daily)
            custom_user.weekly_tasks.set(current_weekly)
            custom_user.monthly_tasks.set(current_monthly)
            custom_user.last_daily_tasks_refreshed = timezone.now()
            custom_user.daily_due_date = timezone.now() + timedelta(days=1)
            custom_user.last_weekly_tasks_refreshed = timezone.now()
            custom_user.weekly_due_date = timezone.now() + timedelta(days=7)
            custom_user.last_monthly_tasks_refreshed = timezone.now()
            custom_user.monthly_due_date = timezone.now() + timedelta(days=30)
            custom_user.save()

        if timezone.now() - custom_user.last_daily_tasks_refreshed > timedelta(days=1):
            for task in custom_user.daily_tasks.all():
                task.completed = False
                task.save()
                # Update subcategory XP
                subcategory = task.subcategory
                subcategory.xp -= task.xp // 2
                subcategory.save()

                # Update category XP
                category = subcategory.category
                category.xp -= task.xp // 2
                category.save()

                # Update user's total XP
                custom_user = CustomUser.objects.get(user=request.user)
                custom_user.total_xp -= task.xp // 2
                custom_user.save()

            # Get user's selected subcategories
            selected_subcats = custom_user.pathway.all()
            subcat_ids = [subcat.id for subcat in selected_subcats]

            # Filter tasks to only selected subcategories
            available_tasks = Task.objects.filter(subcategory__in=subcat_ids, 
                                                completed=False)
            # Shuffle and save new tasks
            if user_difficulty == "Easy":
                daily_tasks = available_tasks.filter(type='daily').order_by('?')[:2]
            elif user_difficulty == "Medium":
                daily_tasks = available_tasks.filter(type='daily').order_by('?')[:3]
            elif user_difficulty == "Hard":
                daily_tasks = available_tasks.filter(type='daily').order_by('?')[:4]
            elif user_difficulty == "ULTIMATE WEAPON":
                daily_tasks = available_tasks.filter(type='daily').order_by('?')[:5]

            custom_user.daily_tasks.set(daily_tasks)
            custom_user.last_daily_tasks_refreshed = timezone.now()
            custom_user.daily_due_date = timezone.now() + timedelta(days=1)

        if timezone.now() - custom_user.last_weekly_tasks_refreshed > timedelta(days=7):
            for task in custom_user.weekly_tasks.all():
                task.completed = False
                task.save()
                # Update subcategory XP
                subcategory = task.subcategory
                subcategory.xp -= task.xp // 2
                subcategory.save()

                # Update category XP
                category = subcategory.category
                category.xp -= task.xp // 2
                category.save()

                # Update user's total XP
                custom_user = CustomUser.objects.get(user=request.user)
                custom_user.total_xp -= task.xp // 2
                custom_user.save()

            # Get user's selected subcategories
            selected_subcats = custom_user.pathway.all()
            subcat_ids = [subcat.id for subcat in selected_subcats]

            # Filter tasks to only selected subcategories
            available_tasks = Task.objects.filter(subcategory__in=subcat_ids, 
                                                completed=False)
            # Shuffle and save new tasks
            if user_difficulty == "Easy":
                weekly_tasks = available_tasks.filter(type='weekly').order_by('?')[:1]
            elif user_difficulty == "Medium":
                weekly_tasks = available_tasks.filter(type='weekly').order_by('?')[:2]
            elif user_difficulty == "Hard":
                weekly_tasks = available_tasks.filter(type='weekly').order_by('?')[:3]
            elif user_difficulty == "ULTIMATE WEAPON":
                weekly_tasks = available_tasks.filter(type='weekly').order_by('?')[:3]

            custom_user.weekly_tasks.set(weekly_tasks)
            custom_user.last_weekly_tasks_refreshed = timezone.now()
            custom_user.weekly_due_date = timezone.now() + timedelta(days=7)

        if timezone.now() - custom_user.last_monthly_tasks_refreshed > timedelta(days=30):
            for task in custom_user.monthly_tasks.all():
                task.completed = False
                task.save()
                # Update subcategory XP
                subcategory = task.subcategory
                subcategory.xp -= task.xp // 2
                subcategory.save()

                # Update category XP
                category = subcategory.category
                category.xp -= task.xp // 2
                category.save()

                # Update user's total XP
                custom_user = CustomUser.objects.get(user=request.user)
                custom_user.total_xp -= task.xp // 2
                custom_user.save()

            # Get user's selected subcategories
            selected_subcats = custom_user.pathway.all()
            subcat_ids = [subcat.id for subcat in selected_subcats]

            # Filter tasks to only selected subcategories
            available_tasks = Task.objects.filter(subcategory__in=subcat_ids, 
                                                completed=False)
            # Shuffle and save new tasks
            if user_difficulty == "Easy":
                monthly_tasks = available_tasks.filter(type='monthly').order_by('?')[:1]
            elif user_difficulty == "Medium":
                monthly_tasks = available_tasks.filter(type='monthly').order_by('?')[:1]
            elif user_difficulty == "Hard":
                monthly_tasks = available_tasks.filter(type='monthly').order_by('?')[:1]
            elif user_difficulty == "ULTIMATE WEAPON":
                monthly_tasks = available_tasks.filter(type='monthly').order_by('?')[:2]

            custom_user.monthly_tasks.set(monthly_tasks)
            custom_user.last_monthly_tasks_refreshed = timezone.now()
            custom_user.monthly_due_date = timezone.now() + timedelta(days=30)

        custom_user.save()        

        daily_tasks = custom_user.daily_tasks.all().values_list('id', flat=True)
        weekly_tasks = custom_user.weekly_tasks.all().values_list('id', flat=True)
        monthly_tasks = custom_user.monthly_tasks.all().values_list('id', flat=True)
        last_daily_tasks_refreshed = custom_user.last_daily_tasks_refreshed
        last_weekly_tasks_refreshed = custom_user.last_weekly_tasks_refreshed
        last_monthly_tasks_refreshed = custom_user.last_monthly_tasks_refreshed
        daily_due_date = custom_user.daily_due_date
        weekly_due_date = custom_user.weekly_due_date
        monthly_due_date = custom_user.monthly_due_date

        return render(request, 'uw_app/player.html', {
            'display_name': custom_user.display_name,
            'character_image': custom_user.character_image,
            'difficulty': custom_user.difficulty,
            'selected_subcats': selected_subcats,
            'total_xp': custom_user.total_xp,
            'daily_tasks': daily_tasks,
            'weekly_tasks': weekly_tasks,
            'monthly_tasks': monthly_tasks,
            'level': custom_user.level,
            'last_daily_refreshed': last_daily_tasks_refreshed,
            'last_weekly_refreshed': last_weekly_tasks_refreshed,
            'last_monthly_refreshed': last_monthly_tasks_refreshed,
            'daily_due_date': daily_due_date,
            'weekly_due_date': weekly_due_date,
            'monthly_due_date': monthly_due_date,
            'current_time': timezone.now(),
        })
    else:
        # Redirect to the home page or display an error message for unauthenticated users
        return redirect('home')

@login_required
def data(request):
    if request.user.is_authenticated:
        custom_user, created = CustomUser.objects.get_or_create(user=request.user)

        categories = Category.objects.all()
        subcategories = Subcategory.objects.all()


        return render(request, 'uw_app/data.html', {
            'display_name': custom_user.display_name,
            'categories': categories,
            'subcategories': subcategories,
            'total_xp': custom_user.total_xp,
        })
    else:
        # Redirect to the home page or display an error message for unauthenticated users
        return redirect('home')


@login_required
def complete_task(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        task_id = request.POST.get('task_id')

        try:
            task = Task.objects.get(id=task_id, completed=False)
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

        user_difficulty = custom_user.difficulty

        # Check if all tasks in 'daily' are completed
        all_daily_tasks_completed = custom_user.daily_tasks.filter(completed=True).count() == custom_user.daily_tasks.count()
        if all_daily_tasks_completed or timezone.now() - custom_user.last_daily_tasks_refreshed > timedelta(days=1):
            for task in custom_user.daily_tasks.all():
                task.completed = False
                task.save()

            # Get user's selected subcategories
            selected_subcats = custom_user.pathway.all()
            subcat_ids = [subcat.id for subcat in selected_subcats]

            # Filter tasks to only selected subcategories
            available_tasks = Task.objects.filter(subcategory__in=subcat_ids, 
                                                completed=False)
            # Shuffle and save new tasks
            if user_difficulty == "Easy":
                daily_tasks = available_tasks.filter(type='daily').order_by('?')[:2]
            elif user_difficulty == "Medium":
                daily_tasks = available_tasks.filter(type='daily').order_by('?')[:3]
            elif user_difficulty == "Hard":
                daily_tasks = available_tasks.filter(type='daily').order_by('?')[:4]
            elif user_difficulty == "ULTIMATE WEAPON":
                daily_tasks = available_tasks.filter(type='daily').order_by('?')[:5]

            custom_user.daily_tasks.set(daily_tasks)
            custom_user.last_daily_tasks_refreshed = timezone.now()
            custom_user.daily_due_date = timezone.now() + timedelta(days=1)

        # Check if all tasks in 'weekly' are completed
        all_weekly_tasks_completed = custom_user.weekly_tasks.filter(completed=True).count() == custom_user.weekly_tasks.count()
        if all_weekly_tasks_completed or timezone.now() - custom_user.last_weekly_tasks_refreshed > timedelta(days=7):
            for task in custom_user.weekly_tasks.all():
                task.completed = False
                task.save()

            # Get user's selected subcategories
            selected_subcats = custom_user.pathway.all()
            subcat_ids = [subcat.id for subcat in selected_subcats]

            # Filter tasks to only selected subcategories
            available_tasks = Task.objects.filter(subcategory__in=subcat_ids, 
                                                completed=False)
            # Shuffle and save new tasks
            if user_difficulty == "Easy":
                weekly_tasks = available_tasks.filter(type='weekly').order_by('?')[:1]
            elif user_difficulty == "Medium":
                weekly_tasks = available_tasks.filter(type='weekly').order_by('?')[:2]
            elif user_difficulty == "Hard":
                weekly_tasks = available_tasks.filter(type='weekly').order_by('?')[:3]
            elif user_difficulty == "ULTIMATE WEAPON":
                weekly_tasks = available_tasks.filter(type='weekly').order_by('?')[:3]

            custom_user.weekly_tasks.set(weekly_tasks)
            custom_user.last_weekly_tasks_refreshed = timezone.now()
            custom_user.weekly_due_date = timezone.now() + timedelta(days=7)

        # Check if all tasks in 'monthly' are completed
        all_monthly_tasks_completed = custom_user.monthly_tasks.filter(completed=True).count() == custom_user.monthly_tasks.count()
        if all_monthly_tasks_completed or timezone.now() - custom_user.last_monthly_tasks_refreshed > timedelta(days=30):
            for task in custom_user.monthly_tasks.all():
                task.completed = False
                task.save()

            # Get user's selected subcategories
            selected_subcats = custom_user.pathway.all()
            subcat_ids = [subcat.id for subcat in selected_subcats]

            # Filter tasks to only selected subcategories
            available_tasks = Task.objects.filter(subcategory__in=subcat_ids, 
                                                completed=False)
            # Shuffle and save new tasks
            if user_difficulty == "Easy":
                monthly_tasks = available_tasks.filter(type='monthly').order_by('?')[:1]
            elif user_difficulty == "Medium":
                monthly_tasks = available_tasks.filter(type='monthly').order_by('?')[:1]
            elif user_difficulty == "Hard":
                monthly_tasks = available_tasks.filter(type='monthly').order_by('?')[:1]
            elif user_difficulty == "ULTIMATE WEAPON":
                monthly_tasks = available_tasks.filter(type='monthly').order_by('?')[:2]

            custom_user.monthly_tasks.set(monthly_tasks)
            custom_user.last_monthly_tasks_refreshed = timezone.now()
            custom_user.monthly_due_date = timezone.now() + timedelta(days=30)

        custom_user.save()

        if subcategory.xp > 1000:
            subcategory.xp = subcategory.xp - 1000
            subcategory.level += 1
            subcategory.save()
        if category.xp > 10000:
            category.xp = category.xp - 10000
            category.level += 1
            custom_user.level += 1
            custom_user.save()
            category.save()

        print('Complete task view completed.')
        return JsonResponse({'success': True, 'message': 'Task completed successfully.'})
    else:
        print('complete_tasks skipped')
        return JsonResponse({'success': False, 'error': 'Invalid request.'})

