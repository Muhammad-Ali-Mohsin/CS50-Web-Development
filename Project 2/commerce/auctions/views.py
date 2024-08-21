from django.contrib.auth import authenticate, login, logout, decorators
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid, Watchlist, Comment, Category
from .forms import NewListingForm, NewBidForm, NewCommentForm


def index(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.filter(closed=False)
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@decorators.login_required
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_price = request.POST["starting_price"]
        image_url = request.POST["image_url"]
        category = Category.objects.get(id=request.POST["category"])
        if not (image_url.endswith(".png") or image_url.endswith(".jpg") or image_url.endswith(".jpeg")):
            image_url = ""

        listing = Listing.objects.create(seller=request.user, title=title, description=description, starting_price=starting_price, image_url=image_url, current_price=starting_price, category=category)
        listing.save()

        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "auctions/create.html", {
            'form': NewListingForm()
        })
    
def view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    sorted_bids = sorted(Bid.objects.filter(listing=listing), key=lambda bid: bid.amount)
    bids = len(sorted_bids)
    current = len(sorted_bids) != 0 and sorted_bids[-1].bidder == request.user

    if listing.closed:
        winner = -1 if sorted_bids == [] else sorted_bids[-1].bidder
    else:
        winner = None

    if request.user.is_authenticated:
        watchlisted = len(Watchlist.objects.filter(user=request.user, listing=listing)) == 1
    else:
        watchlisted = None

    return render(request, "auctions/view.html", {
        'listing': listing,
        'bids': bids,
        'form': NewBidForm(),
        'current': current,
        'watchlisted': watchlisted,
        'is_theirs': listing.seller == request.user,
        'is_closed': listing.closed,
        'winner': winner,
        'comment_form': NewCommentForm(),
        'comments': Comment.objects.filter(listing=listing)
    })

@decorators.login_required
def bid(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        sorted_bids = sorted(Bid.objects.filter(listing=listing), key=lambda bid: bid.amount)
        current = listing.starting_price if sorted_bids == [] else sorted_bids[-1].amount
        amount = float(request.POST["amount"])

        if amount > current:
            bid = Bid.objects.create(bidder=request.user, amount=amount, listing=listing)
            bid.save()
            listing.current_price = amount
            listing.save()
            return HttpResponseRedirect(reverse("view", args=[listing_id]))
        else:
            return render(request, "auctions/error.html", {
                'error': f"Your bid must be higher than the current bid! The current bid is ${current}"
            })
        
@decorators.login_required
def watchlist_add(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        is_watchlisted = len(Watchlist.objects.filter(user=request.user, listing=listing)) == 1

        if is_watchlisted:
            Watchlist.objects.filter(user=request.user, listing=listing).delete()
        else:
            new_watchlist = Watchlist.objects.create(user=request.user, listing=listing)
            new_watchlist.save()

        return HttpResponseRedirect(reverse("view", args=[listing_id]))
    
@decorators.login_required
def close(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    if listing.seller == request.user and not listing.closed:
        listing.closed = True
        listing.save()
        return HttpResponseRedirect(reverse("view", args=[listing_id]))
    elif listing.closed:
        return render(request, "auctions/error.html", {
            'error': f"You can't close this listing as it is already closed."
        })
    else:
        return render(request, "auctions/error.html", {
            'error': f"You can't close this listing as it doesn't belong to you."
        })
    
@decorators.login_required
def comment(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(id=listing_id)
        Comment.objects.create(commenter=request.user, comment=request.POST["comment"], listing=listing)
        return HttpResponseRedirect(reverse("view", args=[listing_id]))

@decorators.login_required
def watchlist(request):
    watchlists = Watchlist.objects.filter(user=request.user)
    listings = [watchlist.listing for watchlist in watchlists]
    return render(request, "auctions/watchlist.html", {
        'listings': listings
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        'categories': Category.objects.all()
    })

def category(request, category_id):
    category_object = Category.objects.get(id=category_id)
    return render(request, "auctions/category.html", {
        'listings': Listing.objects.filter(category=category_id),
        'category': category_object
    })