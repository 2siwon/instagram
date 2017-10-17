from django.db import models


# Create your models here.


class Post(models.Model):
    photo = models.ImageField(upload_to='post')
    created_at = models.DateTimeField(auto_now_add=True)



class PostComment(models.Model):
    # related_name을 적으면 역참조 가능
    # post.postcomment_set.all의 정참조 접근을
    # post.comments.all 로 대신하여 역참조 할 수 있음
    post = models.ForeignKey(
        Post,
        related_name="comments",
    )
    class Meta:
        # 가장 나중에 달린 Comment가 가장 나중에 오도록 ordering설정
        ordering = ['created_at']
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
