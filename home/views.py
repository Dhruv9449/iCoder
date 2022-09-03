from django.shortcuts import render, HttpResponse, redirect
from home.models import Profile, User, Project, Message
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from home.extra_functions.send_message import send_message

# Create your views here.


def home(request):
    """ Home page of the portfolio """
    
    send_message(request)
    posts = Post.objects.order_by('-views')[:2]
    projects = Project.objects.order_by('-sno')[:4]
    context = {'posts': posts, 'projects': projects}
    return render(request, 'home/home.html', context)


def contact(request):
    """ Contact page """
    
    if request.user.is_staff:
        contact_messages = Message.objects.order_by('-datetime').all()
        return render(request, 'home/messages.html', {'contact_messages': contact_messages})
    
    send_message(request)
    if request.method == "POST":
        try:
            name = request.POST['name']
            phone = request.POST['phone']
            email = request.POST['email']
            message = request.POST['message']
            contact = Message(name=name, phone=phone,
                              email=email, message=message)
            contact.save()
            messages.add_message(request, messages.INFO,
                                 'Message sent!', extra_tags=['success', 'Success!'])
        except:
            messages.add_message(request, messages.INFO,
                                 'Please check if you\'ve entered all details correctly and retry. ', 
                                 extra_tags=['danger', 'Error!'])
    return render(request, "home/contact.html")


def projects(request):
    send_message(request)
    projects = Project.objects.order_by('-sno').all()
    context = {'projects': projects}
    return render(request, "home/projects.html", context)


@login_required
def view_profile(request):
    send_message(request)
    if request.method == "POST":
        try:
            user = request.user
            profile = Profile.objects.get(user=user)
            user.first_name = request.POST['edit_first_name']
            user.last_name = request.POST['edit_last_name']
            user.email = request.POST['edit_email']
            profile_picture = request.FILES.get('edit_profile_picture', False)
            if profile_picture:
                profile.profile_picture = profile_picture
            user.save()
            profile.save()
            messages.add_message(request, messages.INFO, 'Profile updated successfully!', extra_tags=['success', 'Success!'])
                        
            
        except:
            messages.add_message(request, messages.INFO,
                                 'Please check if you\'ve entered all details correctly and retry. ', 
                                 extra_tags=['danger', 'Error!'])
            
    
    return render(request, 'home/profile.html')


@staff_member_required(login_url='/')
def new_project(request):
    """ Add new project """
    if request.method == "POST":
        # try:
        name = request.POST.get('name','')
        desc = request.POST.get('description','')
        link = request.POST.get('link','')
        start_date = request.POST.get('startdate','')
        finish_date = request.POST.get('enddate','')                
        project = Project(name=name, desc=desc, link=link, start_date=start_date, finish_date=finish_date)
        thumbnail = request.FILES.get('thumbnail', False)
        if thumbnail:
            project.thumbnail = thumbnail
        project.save()
        messages.add_message(request, messages.INFO, 'Added project successfully!', extra_tags=['success', 'Success!'])
        
        # except:
        #     messages.add_message(request, messages.INFO,
        #                          'Please check if you\'ve entered all details correctly and retry. ', 
        #                          extra_tags=['danger', 'Error!'])
                 
    return render(request, 'home/newproject.html')



# Authentication APIs
def handle_signup(request):
    if request.method == 'POST':
        username = request.POST['signup_username']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        password = request.POST['signup_password']
        email = request.POST['email']

        if User.objects.filter(username=username).exists():
            request.session['message'] = {
                'message_text': 'Please try another username.', 'extra_tags': ['danger', 'Username already taken!']}

        elif User.objects.filter(email=email).exists():
            request.session['message'] = {
                'message_text': 'An account with the email already exists.', 'extra_tags': ['danger', 'Email already in use!']}

        else:
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                first_name = fname,
                last_name = lname
                )
            profile = Profile(user=user)
            user.save()
            profile.save()
            request.session['message'] = {
                'message_text': 'Account created.', 'extra_tags': ['success', 'Success!']}

    else:
        return HttpResponse('404 -  Not Found')
    return redirect('/', {})


def handle_login(request):
    
    """ Login and authentication"""
    
    if request.method == 'POST':
        username = request.POST['login_username']
        password = request.POST['login_password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['message'] = {
                'message_text': 'Logged into your account.', 'extra_tags': ['success', 'Success!']}

        else:
            request.session['message'] = {
                'message_text': 'Could not find an account, please sign-up if you don\' have an acount.', 'extra_tags': ['danger', 'Invalid credentials!']}
        return redirect('/')
    else:
        return HttpResponse('404 -  Not Found')


def handle_logout(request):
    """ Handles logout """
    
    logout(request)
    request.session['message'] = {
        'message_text': 'Logged out of your account.', 'extra_tags': ['success', 'Success!']}
    return redirect('/')
