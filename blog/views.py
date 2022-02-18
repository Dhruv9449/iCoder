from django.shortcuts import render, HttpResponse
from blog.models import Post
from django.db.models import Q
from django.contrib import messages

# Create your views here.


def blogHome(request):
    allPosts = Post.objects.order_by('-upload_date')
    context = {'posts': allPosts}
    return render(request, "blog/bloghome.html", context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views += 1
    post.save()
    context = {'post': post}
    return render(request, "blog/blogpost.html", context)


def search(request):
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
