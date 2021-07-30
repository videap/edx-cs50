from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

category_choices = [
    ("AUTO", 'Automotive'),
    ("EL", 'Electronics'),
    ("ART", 'Arts'),
    ("SPT", 'Sports'),
    ("FSH", 'Fashion'),
    ("HME", 'Home'),
    ("RE", 'Real Estate'),
    ("PET", 'Pets'),
    ("IND", 'Industry'),
    ("KID", "Kids")
]

class Listing(models.Model):

    title = models.CharField(max_length=64)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_listings")
    image_url = models.URLField(blank=True)
    description = models.TextField(max_length=2048)
    open_status = models.BooleanField(default=True)
    min_bid = models.DecimalField(max_digits=11, decimal_places=2)
    category = models.CharField(max_length=24, choices=category_choices)
    creation_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: {self.title}"


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_bids")
    bid_value = models.DecimalField(max_digits=11, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}: ${self.bid_value}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_comments")
    content = models.TextField(max_length=256)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.timestamp}"


class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, related_name="users_watching", blank=True)

    def __str__(self):
        return f"{self.id}: {self.username}"

class Winner(models.Model):
    listing = models.OneToOneField(Listing, on_delete=models.CASCADE)
    bid = models.OneToOneField(Bid, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} won {self.listing} for {self.bid}"