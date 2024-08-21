
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("get_posts", views.get_posts, name="get_posts"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("get_followers", views.get_followers, name="get_followers"),
    path("like", views.like, name="like"),
    path("edit_post", views.edit_post, name="edit_post")
]
