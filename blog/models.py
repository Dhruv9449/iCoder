from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=254)
    desc = models.TextField()
    content = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    views = models.BigIntegerField(default=0)
    slug = models.SlugField(
        max_length=200, editable=True, null=True, blank=True)
    thumbnail = models.ImageField(upload_to="blog/images/")

    def __str__(self):
        return str(self.sno) + ". " + self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super(Post, self).save(*args, **kwargs)


class BlogComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="blog_comments")
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, related_name="replies")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Post: " + str(self.post.sno) + " by " + self.user.username
