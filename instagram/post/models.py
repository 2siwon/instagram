from django.conf import settings
from django.db import models


# Create your models here.

class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(author=None)


class Post(models.Model):
    # author = models.ForeignKey(User)
    # 직접 유저 모델을 불러왔을 때랑 어떤 이점이?
    # 이름이 바뀌어도 되고 기본모델이건 커스텀모델이건 상관없음
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    photo = models.ImageField(upload_to='post')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    class Meta:
        ordering = ['-created_at']


class PostComment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    # related_name을 적으면 역참조 가능
    # post.postcomment_set.all의 정참조 접근을
    # post.comments.all 로 대신하여 역참조 할 수 있음
    post = models.ForeignKey(Post, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 가장 나중에 달린 Comment가 가장 나중에 오도록 ordering설정
        ordering = ['created_at']
