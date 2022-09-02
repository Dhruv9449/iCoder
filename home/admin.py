from django.contrib import admin
from home.models import Project, Profile, Message

# Register your models here.
admin.site.register(Message)
admin.site.register(Project)
admin.site.register(Profile)
