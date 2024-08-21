from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(max_length=256, default="Post Content")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self, user=None):
        return {
            'id': self.id,
            'content': self.content,
            'author': self.author.username,
            'timestamp': self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            'likes': len(Like.objects.filter(post=self)),
            'is_liked': False if user == None else len(Like.objects.filter(post=self, liker=user)) == 1
        }

class Like(models.Model):
    id = models.AutoField(primary_key=True)
    liker = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Follow(models.Model):
    id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followee")

