from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact, Project
from blog.models import Post
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def home(request):
    if ('message' in request.session):
        message = request.session['message']
        messages.add_message(
            request, messages.INFO, message['message_text'], extra_tags=message['extra_tags'])
        del request.session['message']
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


def handleSignup(request):
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
                username=username, email=email, password=password)
            user.first_name = fname
            user.last_name = lname
            user.save()
            request.session['message'] = {
                'message_text': 'Account created.', 'extra_tags': ['success', 'Success!']}

    else:
        return HttpResponse('404 -  Not Found')
    return redirect('/', {})

# Authentication API


def handleLogin(request):
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


def handleLogout(request):
    logout(request)
    request.session['message'] = {
        'message_text': 'Logged out of your account.', 'extra_tags': ['success', 'Success!']}
    return redirect('/')
