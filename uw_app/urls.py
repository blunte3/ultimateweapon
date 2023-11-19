from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('signout', views.signout, name="signout"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('', views.index, name="index"),
    path('settings', views.settings, name="settings"),
    path('player', views.player, name="player"),
     path('complete-task', views.complete_task, name='complete_task'),
]