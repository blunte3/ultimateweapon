# Ultimate Weapon: Master Your Life

Welcome to Ultimate Weapon, a revolutionary game-ify life task website designed to transform your journey of self-improvement into an epic quest. The ultimate goal? Attain proficiency or mastery in every conceivable skill and area of knowledge, becoming the ultimate weapon in the game of life.

## Overview

Ultimate Weapon is not just another productivity tool; it's a dynamic and engaging platform that turns personal development into a thrilling adventure. Whether you're aiming to enhance your professional skills, learn a new language, adopt healthier habits, or explore new realms of knowledge, this game empowers you to conquer life's challenges and level up in every aspect.

## Key Features

### 1. Gamified Task Management

Embark on a quest to conquer various life tasks, each representing a unique skill or area of knowledge. Earn experience points (XP) and level up as you successfully complete tasks, unlocking new challenges and achievements.

### 2. Progress Bars and Specializations

Dive into progress bars that represent different categories such as professional skills, personal development, fitness, creativity, and more. Choose your path wisely, specializing in areas that align with your personal goals.

### 3. Collaborative Challenges

Join forces with friends, family, or fellow users to tackle collaborative challenges. Strengthen your social connections while collectively striving for mastery in specific domains.

### 4. Progress Tracking and Analytics

Monitor your growth with detailed progress tracking and analytics. Visualize your achievements, identify areas for improvement, and celebrate your milestones on the road to becoming the ultimate weapon.

### 5. Dynamic Rewards System

Earn rewards for completing tasks and achieving milestones. Customize your virtual avatar, unlock in-game bonuses, and enjoy a sense of accomplishment as you watch your virtual self evolve.

### 6. Community and Leaderboards

Connect with a vibrant community of like-minded individuals. Share tips, support each other, and compete on leaderboards to see who can truly claim the title of the ultimate weapon.

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/your-username/ultimate-weapon.git
```

## Set Up Your Environment
Using a venv is recommended but is not necessary.

Install necessary dependencies:
```bash
pip install Django
pip install psycopg2
```
To generate all categories, tasks, and reminders, run in order:
```bash
python manage.py create_categories
python manage.py create_subcategories
python manage.py create_subsubcategories
python manage.py create_tasks
python manage.py create_reminders
```
If you change any of the data in these files for additions re-run the commands depending on what you changed in order for them to update.

Finally run the website using:
```bash
python manage.py runserver
```

Additionally, if there are any changes to the models file. The changes will not showup until you run:
```bash
python manage.py makemigrations uw_app
python manage.py migrate uw_app
```

## Create Your Avatar
Customize your virtual avatar and begin your journey to mastering every skill in the game of life.

## Contribute and Improve
Join the community of contributors, share your ideas, and enhance the Ultimate Weapon experience for everyone.

## Let the Quest Begin
Are you ready to transform your life into an extraordinary adventure? Clone the Ultimate Weapon repository, embark on your journey, and become the ultimate weapon in the game of life! May your skills be sharp, and your knowledge boundless.
