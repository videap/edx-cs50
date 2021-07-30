from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='profile_images', blank=True) 

class Post(models.Model):
    post_owner = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_posts")
    post_content = models.TextField(max_length=255, blank=False)
    post_creation = models.DateTimeField(auto_now_add=True)
    post_last_change = models.DateTimeField(auto_now=True)

class Like(models.Model):
    like_post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="post_likes")
    like_user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user_likes")
    like_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["like_post_id", "like_user"]

class Follower(models.Model):
    user_a_followed_by_b = models.ForeignKey("User", on_delete=models.CASCADE, related_name="a_is_followed_by")
    user_b_follows_a = models.ForeignKey("User", on_delete=models.CASCADE, related_name="b_is_following")

    class Meta:
        unique_together = ["user_a_followed_by_b", "user_b_follows_a"]