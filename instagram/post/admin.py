from django.contrib import admin

# Register your models here.
from .models import PostComment, Post



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['photo', 'created_at']


@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['post_id', 'content', 'created_at']