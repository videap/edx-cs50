from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("feed", views.feed, name="feed"),
    path("following", views.feed, name="following"),
    path("get_posts", views.get_posts, name="get_posts"),
    path("get_post_info", views.get_post_info, name="get_post_info"),
    path("follow_unfollow", views.follow_unfollow, name="follow_unfollow"),
    path("update_post", views.update_post, name="update_post"),
    path("like_dislike", views.like_dislike, name="like_dislike"),
    path("<str:username>", views.user_page, name="user_page"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

