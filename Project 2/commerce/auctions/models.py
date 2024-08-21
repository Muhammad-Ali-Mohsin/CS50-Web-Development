from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(max_length=64, default="Category Name")
    description = models.TextField(max_length=256, default="Category Description")

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_price = models.DecimalField(max_digits=16, decimal_places=2)
    title = models.TextField(max_length=64, default="Listing Title")
    description = models.TextField(max_length=256, default="Auction Listing")
    image_url = models.TextField(default="")
    current_price = models.DecimalField(max_digits=16, decimal_places=2)
    closed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=256)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    time_created = models.TimeField(auto_now=True)

class Watchlist(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

