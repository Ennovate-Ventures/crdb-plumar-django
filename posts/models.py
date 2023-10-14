from django.db import models
from userauth.models import Profile

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=128)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)   
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to='post_images', null = True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)   
    content = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return str(self.user.username)