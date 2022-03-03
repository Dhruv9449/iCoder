from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path('', views.blogHome, name="blogHome"),
    path('postcomment', views.postComment, name="postComment"),
    path('newpost', views.newpost, name="newpost"),
    path('<str:slug>', views.blogPost, name="blogPost"),
    path('search/', views.search, name="search")
]
