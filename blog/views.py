from django.shortcuts import render, HttpResponse, redirect
from blog.models import BlogComment, Post
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from blog.templatetags import custom_tags
from home.extra_functions.send_message import send_message

# Create your views here.


def blog_home(request):
    send_message(request)
    allPosts = Post.objects.order_by('-upload_date')
    context = {'posts': allPosts}
    return render(request, "blog/bloghome.html", context)


def blog_post(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views += 1
    post.save()
    context = {'post': post}
    send_message(request)
    return render(request, "blog/blogpost.html", context)


def search(request):
    send_message(request)
    query = request.GET['query']
    if len(query) > 78:
        result_posts = Post.objects.none()
    else:
        result_posts = Post.objects.filter(Q(title__icontains=query) | Q(
            content__icontains=query) | Q(desc__icontains=query)).order_by('-upload_date')

    if result_posts.count() == 0:
        messages.add_message(request, messages.INFO,
                             'Please enter valid queries in search.', extra_tags=['warning', 'No results found!'])
    context = {'posts': result_posts, 'query': query}
    return render(request, "blog/search.html", context)


@staff_member_required(login_url='/')
def new_post(request):
    if request.user.is_staff:
        if request.method == "POST":
            title = request.POST['title']
            desc = request.POST['description']
            thumbnail = request.FILES['thumbnail']
            content = request.POST['content']

            print("Thumbnail")
            post = Post(title=title, desc=desc,
                        thumbnail=thumbnail, content=content)
            post.save()

            request.session['message'] = {
                'message_text': 'Posted new blog!', 'extra_tags': ['success', 'Success!']}

            return redirect("/blog", {})
        return render(request, "blog/newpost.html")
    
    return HttpResponse('404 - Not Found')


# Comments API
@login_required
def post_comment(request):
    if request.method == 'POST':
        comment = request.POST['comment_input']
        user = request.user
        post_sno = request.POST['post_sno']
        post = Post.objects.get(sno=post_sno)
        parent_sno = request.POST['comment_sno']

        if parent_sno == '':
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            request.session['message'] = {
                'message_text': 'Comment added.', 'extra_tags': ['success', 'Success!']}
        else:
            parent = BlogComment.objects.get(sno=parent_sno)
            reply = BlogComment(comment=comment, user=user,
                                post=post, parent=parent)
            reply.save()
            request.session['message'] = {
                'message_text': 'Reply added.', 'extra_tags': ['success', 'Success!']}

    return redirect(f'/blog/{post.slug}', {})
