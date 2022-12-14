from django.contrib import admin
from .models import *

class auction(admin.ModelAdmin):
    list_display = ("id", "title", "active_bool", "starting_bid", "start_time", "end_time", "image_url" )

class bids(admin.ModelAdmin):
    list_display = ("id", "user", "list_id", "bid")

# Register your models here.
admin.site.register(auctionlist, auction)
admin.site.register(bidders, bids)
admin.site.register(User)