from django.contrib import admin
from .models import Posts, Comment


# Register your models here.
@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "image", "caption", "created_at", "updated_at")
    list_filter = ("user", "created_at", "updated_at")
    search_fields = ("user", "caption")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "comment", "created_at", "updated_at")
    list_filter = ("user", "post", "created_at", "updated_at")
    search_fields = ("user", "post")
