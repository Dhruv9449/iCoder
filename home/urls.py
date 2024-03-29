from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('contact', views.contact, name="contact"),
    path('newproject', views.new_project, name="new project"),
    path('projects', views.projects, name="projects"),
    path('signup', views.handle_signup, name="signup"),
    path('profile', views.view_profile, name="profile"),
    path('login', views.handle_login, name='login'),
    path('logout', views.handle_logout, name='logout')
]
