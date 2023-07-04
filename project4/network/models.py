from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default-avatar.jpg')

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.text}"
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked")
    time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user} liked {self.post}"