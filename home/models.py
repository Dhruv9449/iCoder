from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Message from ' + self.name


class Project(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    desc = models.TextField()
    link = models.URLField(max_length=500)
    thumbnail = models.ImageField(upload_to='home/images')


def upload_location(instance, filename):
    extension = filename.split('.')
    return f'users/profile_pictures/{instance.user.username}.{extension[-1]}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to=upload_location, default='users/defaults/profile_pic.png')

    def __str__(self):
        return self.user.username
