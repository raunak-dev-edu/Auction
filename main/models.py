from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class auctionlist(models.Model):
    title = models.CharField(max_length=64)
    image_url = models.CharField(max_length=228, default = None, blank = True, null = True)
    starting_bid = models.IntegerField()  
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)  
    active_bool = models.BooleanField(default = True)

    def __str__(self):
        return f"{self.title}"

class bidders(models.Model):
    user = models.CharField(max_length=64)
    list_id = models.IntegerField()
    bid = models.IntegerField()