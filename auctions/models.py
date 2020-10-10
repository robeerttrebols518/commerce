from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Watchlist(models.Model):
    user = models.CharField(max_length=70)
    listingid = models.IntegerField()

class Listing(models.Model):
    owner = models.CharField(max_length=70)
    title = models.CharField(max_length=70)
    description = models.TextField()
    price = models.IntegerField()
    category = models.CharField(max_length=70)
    link = models.CharField(max_length=70,default=None,blank=True,null=True)
    time = models.CharField(max_length=70)

class Listtotal(models.Model):
    listingid = models.IntegerField()
    title = models.CharField(max_length=64)
    description = models.TextField()
    link = models.CharField(max_length=64,default=None,blank=True,null=True)

class Comment(models.Model):
    user = models.CharField(max_length=64)
    time = models.CharField(max_length=64)
    comment = models.TextField()
    listingid = models.IntegerField()

class Bid(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    listingid = models.IntegerField()
    bid = models.IntegerField()

class Auctionclosed(models.Model):
    owner = models.CharField(max_length=64)
    winner = models.CharField(max_length=64)
    listingid = models.IntegerField()
    winprice = models.IntegerField()