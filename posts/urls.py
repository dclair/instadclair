from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("create/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/<int:post_id>/like/", views.like_post, name="like_post"),
    path("post/like-ajax/<int:pk>/", views.like_post_ajax, name="like_post_ajax"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
]
