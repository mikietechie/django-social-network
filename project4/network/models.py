from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE,related_name='poster')
    msg = models.TextField(max_length=10000)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.user} : {self.msg} @ {self.timestamp}"
    
    def serialize(self):
        return {
            'id':self.id,
            'user':str(self.user),
            'msg':self.msg,
            'likes': self.likes,
            'dislikes': self.dislikes,
            'self': self.__str__()
        }
    

class Comment(models.Model):
    post = models.ForeignKey('Post',on_delete=models.CASCADE,related_name='post')
    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name='commentor')
    comment = models.CharField(max_length=5000)
    def __str__(self):
        return f"{self.user.username} said {self.comment} on {self.post}"
    
    def serialize(self):
        return {
            'id':self.id,
            'user':str(self.user),
            'comment':self.msg,
            'self': self.__str__()
        }

class Follow(models.Model):
    user = models.ForeignKey('User',on_delete=models.CASCADE,related_name='user')
    follower= models.ForeignKey('User',on_delete=models.CASCADE,related_name='follower')
    def __str__(self):
        return f"{self.follower.username} follows {self.user.username}"
    
    def serialize(self):
        return {
            'id':self.id,
            'user':str(self.user),
            'follower':str(self.follower),
            'self': self.__str__()
        }
    


