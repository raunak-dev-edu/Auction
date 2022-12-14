from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Max
from django.utils import timezone

def index(request):
    current_time = timezone.now()
    # check if auction is started
    for i in auctionlist.objects.filter(active_bool=True):
        if i.start_time <= current_time:
            i.active_bool = True
            i.save()

    # check if auction is over
    for i in auctionlist.objects.filter(active_bool=True):
        if i.end_time <= current_time:
            i.active_bool = False
            i.save()

    # get winner
    winner = None
    for i in auctionlist.objects.filter(active_bool=False):
        if bidders.objects.filter(list_id=i.id).exists():
            winner = bidders.objects.filter(
                list_id=i.id).aggregate(Max('bid'))['bid__max']
            winner = bidders.objects.get(bid=winner).user
            i.winner = winner
            i.save()
        

    return render(request, "index.html", {
        "a1": auctionlist.objects.all(),
        "winner": winner,
    })

 
def login_view(request):
    if request.method == "POST":

        # sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # check password confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # check if username/password is empty
        if username == '' or password == '':
            return render(request, "register.html", {
                "message": "Please enter a username and password."
            })
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # create new user
        try:
            user = User.objects.create_user(username, password)
            user.set_password(password)
            user.save()
        except IntegrityError:
            return render(request, "register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "register.html")


@login_required(login_url='login')
def bid(request):
    if request.method == "POST":
        bid = request.POST["bid_amnt"]
        list_id = request.POST["list_id"]
        user = request.user
        # check if auction is started
        if auctionlist.objects.get(id=list_id).start_time <= timezone.now():
            auctionlist.objects.filter(id=list_id).update(active_bool=True)
        else:
            messages.error(request, 'Auction has not started yet!')
            return redirect('index')
        # check if bid is empty
        if bid == '':
            messages.error(request, 'Please enter a bid!')
            return redirect('index')
        else:
            # check if bid is higher than current bid
            if int(bid) > auctionlist.objects.get(id=list_id).starting_bid:
                # check if bid is higher than previous bid
                if bidders.objects.filter(list_id=list_id).exists():
                    if int(bid) > bidders.objects.filter(list_id=list_id).aggregate(Max('bid'))['bid__max']:
                        bidders.objects.create(user=user, list_id=list_id, bid=bid)
                        messages.success(request, 'Bid successfully placed!')
                        return redirect('index')
                    else:
                        messages.error(
                            request, 'Bid must be higher than previous bid!')
                        return redirect('index')
                else:
                    bidders.objects.create(user=user, list_id=list_id, bid=bid)
                    messages.success(request, 'Bid successfully placed!')
                    return redirect('index')
            else:
                messages.error(request, 'Bid must be higher than current bid!')
                return redirect('index')
    else:
        return redirect('index')