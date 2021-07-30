from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("listing/<int:listing_id>", views.listing_page, name="listing_page"),
    path("<int:listing_id>/add_remove", views.add_remove_watchlist, name="add_remove"),
    path("<int:listing_id>/close", views.close_listing, name="close_listing"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("comment/<int:listing_id>", views.comment_listing, name="comment_listing"),
    path("categories", views.categories, name="categories")
]
