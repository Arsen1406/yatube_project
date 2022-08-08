import imp
from operator import mod
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model() 

class Post(models.Model):
    text_post = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author_post = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='posts'
        )
