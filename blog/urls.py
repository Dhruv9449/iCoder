from django.contrib import admin
from django.urls import path, include
from blog import views

urlpatterns = [
    path('', views.blog_home, name="blog home"),
    path('postcomment', views.post_comment, name="post comment"),
    path('newpost', views.new_post, name="new post"),
    path('<str:slug>', views.blog_post, name="blog post"),
    path('search/', views.search, name="search")
]
