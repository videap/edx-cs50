from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
import decimal

from auctions.forms import *
from auctions.functions import *
from auctions.models import *


def index(request):
    if request.GET.get("category", False):
        open_listings = Listing.objects.filter(open_status=True, category=request.GET["category"])
        title = "Category: " + request.GET["name"]
    else:
        open_listings = Listing.objects.filter(open_status=True)
        title = "Active Listings"
    
    return render(request, "auctions/index.html", {
        "open_listings": get_current_bid(open_listings),
        "page_title": title
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
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password, first_name=first_name.capitalize(), last_name=last_name.capitalize())
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
     
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        image_url = request.POST['image_url']
        min_bid = request.POST['min_bid']
        category = request.POST.get('category', False)

        if image_url == "":
            image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/1024px-No_image_available.svg.png"

        try:
            Listing.objects.create(title=title, owner=request.user, description=description, category=category, image_url=image_url, min_bid=min_bid)
        except ValueError:
            return HttpResponseBadRequest("Form is invalid")

        return HttpResponseRedirect(reverse("index"))
        
    else:
        form = NewListingForm()

        return render(request, "auctions/create_listing.html", {
            "new_listing_form": form
        })

@login_required
def watchlist(request):
    num_items=20
    watchlist_listings = get_user_watchlist(request.user.id)

    return render(request, "auctions/watchlist.html", {
        "watchlist_listings": get_current_bid(watchlist_listings)
    })

def listing_page(request, listing_id):

    #Get the max bid and add to the listing as property (annotate to queryset)
    listing = Listing.objects.filter(id=listing_id)
    listing = get_current_bid(listing)[0]

    if listing.current_bid == None:
        listing.current_bid = listing.min_bid

    #if the method is POST, the user is placing a bid
    if request.method == "POST":

        bid_value = decimal.Decimal(request.POST["bid_value"])
        
        #check if the bid is actually the highest
        if bid_value > get_current_bid_value(listing_id):
            try:
                Bid.objects.create(user_id=request.user.id, listing_id=listing_id, bid_value=bid_value)
            except IntegrityError:
                return HttpResponseBadRequest("Form is invalid: Database Error.")    
            return HttpResponseRedirect(reverse("listing_page", kwargs = {"listing_id": listing_id}))

        else: return HttpResponseBadRequest("The bid must be higher than the current bid.")

    #if the request is GET:
    else:   

        #add/remove from watchlist parameters
        watchlist = get_user_watchlist(request.user.id)
        users_watching = list(Listing.objects.filter(id=listing_id).values_list("users_watching", flat=True))
        user_is_watching = True if request.user.id in users_watching else False

        #check if the user is the owner
        owner = Listing.objects.get(id=listing_id).owner_id
        user_is_owner = True if owner == request.user.id else False

        #check if the user has the winning bid
        try:
            current_bid_user = Winner.objects.get(listing_id=listing_id).user_id
            user_is_winner = True if current_bid_user == request.user.id else False
        except ObjectDoesNotExist:
            user_is_winner = False

        #load comments
        Comments = Comment.objects.filter(listing_id=listing_id)

        return render(request, "auctions/listing_page.html", { 
            "listing": listing,
            "user_is_watching": user_is_watching,
            "user_is_owner": user_is_owner,
            "user_is_winner": user_is_winner,
            "Comments": Comments,
        })

@login_required
def add_remove_watchlist(request, listing_id):
    watchlist = get_user_watchlist(request.user.id)
    new_watchlist = []

    #if the listing is not in the watchlist, add it
    if listing_id not in watchlist.values_list("id", flat=True):
        User.objects.get(id=request.user.id).watchlist.add(listing_id)
        return HttpResponseRedirect(reverse("listing_page", kwargs={"listing_id": listing_id }))
    
    #if the listing is in the watchlist, remove it
    else:
        User.objects.get(id=request.user.id).watchlist.remove(listing_id)
        return HttpResponseRedirect(reverse("listing_page", kwargs={"listing_id": listing_id }))

@login_required
def close_listing(request, listing_id):
    #check if the user is the owner
    is_owner = True if Listing.objects.get(id=listing_id).owner_id == request.user.id else False

    #check if the auction is still open
    is_open = True if Listing.objects.get(id=listing_id).open_status == True else False

    #check if there is a valid bid (value-listing) 
    try:
        bid = Bid.objects.get(listing_id=listing_id, bid_value=get_current_bid_value(listing_id))
        bid_is_valid = True
    except ObjectDoesNotExist:
        bid_is_valid=False
    

    #if all conditions are met
    if is_open and is_owner:
        try:
            #update the Listing Model
            listing = Listing.objects.get(id=listing_id)
            listing.open_status = False
            listing.save()

            if bid_is_valid:
                #update the Winners Model
                Winner.objects.create(user_id=bid.user_id, listing_id=listing_id, bid_id=bid.id)

        except IntegrityError:
            return HttpResponseBadRequest("Database Error")

        return HttpResponseRedirect(reverse("listing_page", kwargs = {"listing_id": listing_id}))
    
    else:
        return HttpResponseRedirect(reverse("listing_page", kwargs = {"listing_id": listing_id}))

@login_required
def my_listings(request):
    #the list of the first 20 objects, and current bid
    num_items=20
    open_listings = Listing.objects.filter(owner_id=request.user.id)[:num_items]
    
    return render(request, "auctions/index.html", {
        "open_listings": get_current_bid(open_listings),
        "page_title": "My Listings for Auction"
    })

@login_required
def comment_listing(request, listing_id):
    if request.method == "POST":
        content=str(request.POST["content"])
        Comment.objects.create(user_id=request.user.id, listing_id=listing_id, content=content)

        try:
            return HttpResponseRedirect(reverse("listing_page", kwargs={"listing_id": listing_id}))
        except IntegrityError:
            return HttpResponseBadRequest("Comment is invalid")
    else:
        return HttpResponseRedirect(reverse("listing_page", kwargs={"listing_id": listing_id}))

def categories(request):
    #the list of the first 20 objects, and current bid
    num_items=20
    
    return render(request, "auctions/categories.html", {
        "categories": category_choices,
        "page_title": "Categories"
    })









