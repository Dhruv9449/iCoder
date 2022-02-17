from django.shortcuts import render, HttpResponse
from home.models import Contact, Project
from blog.models import Post
from django.contrib import messages

# Create your views here.


def home(request):
    posts = Post.objects.order_by('-views')[:2]
    projects = Project.objects.all()[:4]
    context = {'posts': posts, 'projects': projects}
    return render(request, 'home/home.html', context)


def about(request):
    return render(request, "home/about.html")


def contact(request):
    if request.method == "POST":
        try:
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            message = request.POST['message']
            contact = Contact(name=name, phone=phone,
                              email=email, message=message)
            contact.save()
            messages.add_message(request, messages.INFO,
                                 'Message sent!', extra_tags=['success', 'Success!'])
        except:
            messages.add_message(request, messages.INFO,
                                 'Please check if you\'ve entered all details correctly and retry. ', extra_tags=['danger', 'Error!'])
    return render(request, "home/contact.html")


def projects(request):
    return render(request, "home/projects.html")
