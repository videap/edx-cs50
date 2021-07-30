from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


class BidsInline(admin.TabularInline):
    model = Bid

class CommentsInline(admin.TabularInline):
    model = Comment

class WinnersInline(admin.TabularInline):
    model=Winner

class ListingAdm(admin.ModelAdmin):
    inlines = [
        BidsInline,
        CommentsInline,
        WinnersInline,  
    ]

class UserAdm(admin.ModelAdmin):
    filter_horizontal = ("watchlist",)

    inlines = [
        BidsInline,
        CommentsInline,
    ]


# Register your models here.
admin.site.register(User, UserAdm)
admin.site.register(Listing, ListingAdm)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Winner)