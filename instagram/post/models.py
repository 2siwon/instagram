from django.db import models


# Create your models here.


class Post(models.Model):
    photo = models.ImageField(upload_to='post')
    # setting.py에
    created_at = models.DateTimeField(auto_now_add=True)


class PostComment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name="comment",
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
