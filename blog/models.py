from django.db import models
from django.contrib.auth.models import User
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.title
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author= models.CharField(max_length=80)
    text = models.TextField(max_length=100)
    created_at= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Comment by {self.author}'


# Create your models here.
