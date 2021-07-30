from auctions.models import *
from django.db.models import Max


def get_current_bid(listing_as_queryset):
    #this function appends the maximum bid value and id for each listing of a QuerySet as an attribute "current_bid"
    #if there is no bid, it returns None
    listing_with_current_bid = listing_as_queryset.annotate(current_bid=Max("listing_bids__bid_value"))
    return listing_with_current_bid


def get_current_bid_value(listing_id):
    initial_bid = Listing.objects.get(id=listing_id).min_bid
    current_bid = Bid.objects.filter(listing_id=listing_id).aggregate(Max("bid_value"))["bid_value__max"]

    if current_bid == None:
        return initial_bid
    else:
        return max(current_bid, initial_bid)



def get_user_watchlist(user_id):
    #this function returns all listing objects from a user wathclist as queryset, filtering a number of items
    watchlist_ids_list = User.objects.filter(id=user_id).values_list("watchlist", flat=True)  
    return Listing.objects.filter(id__in=watchlist_ids_list)


