import json
from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotFound, HttpResponseRedirect, HttpResponseServerError,
                         JsonResponse)
from django.shortcuts import render
from django.urls import reverse

from .models import *


def paginate(post_ids, page_number):
    p = Paginator(post_ids, 10)
    page = p.page(page_number)

    pagination = {
        'num_pages':int(p.num_pages),
        'page': str(page),
        'has_previous': bool(page.has_previous()),
        'has_next': bool(page.has_next()),
        'page_num':int(page_number),
        'post_ids': list(page.object_list)
    }
    return pagination



#check if user a is followed by user b, if true, returns tuple (True, id_in_Model)
def a_is_followed_by_b(a, b):
    try:
        follower_id = Follower.objects.get(user_a_followed_by_b__username=a, user_b_follows_a__username=b).id
        return (True, follower_id)
    except Follower.DoesNotExist:
        return (False, None)


def get_user_info(username, request_user):
    usr = User.objects.get(username=username)
    if a_is_followed_by_b(username, request_user)[0]: 
        follow_btn="Unfollow"  
    else: 
        follow_btn="Follow"

    return {
            "pageuser": usr,
            "post_num": len(usr.user_posts.values_list(flat=True)),
            "followed_by_num": len(usr.a_is_followed_by.values_list(flat=True)),
            "following_num": len(usr.b_is_following.values_list(flat=True)),
            "follow_btn": follow_btn,
        }


def index(request):
    if request.method == "POST":
        pass

    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('feed'))

    else:
        return render(request, "network/index.html")


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def feed(request):
        #POST methods are for new posts (create)
    if request.method == 'POST':
        post_text = str(request.POST.get('post_text'))
        new_post = Post(post_owner=request.user, post_content=post_text)
        try:
            new_post.save()
            return HttpResponseRedirect(reverse('feed'))
        except IntegrityError:
            return HttpResponse('Error saving your post. Please try again later.')

    else:
        usr_info = get_user_info(request.user.username, request.user.username)
        return render(request, "network/user.html", usr_info)

@login_required
def user_page(request, username):
    #check if username exists
    try:
        usr_info = get_user_info(username, request.user.username)
        return render(request, "network/user.html", usr_info)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))

# API TO FETCH POSTS VISIBLE TO USER
@login_required
def get_posts(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400) # BAD REQUEST RESPONSE
    else:
        
        if 'page' in request.GET and request.GET['page']:
            page_num = request.GET['page']
        else:
            page_num = 1
        
        #check if request is from the following page:
        if request.GET.get('following'):
            following_users = User.objects.get(id=request.user.id).b_is_following.values_list('user_a_followed_by_b_id',flat=True)
            post_ids = list(User.objects.filter(id__in=following_users).values_list('user_posts__id', flat=True).order_by('-user_posts__post_creation'))
            if post_ids == []:
                return JsonResponse({"NoPosts": "The users you follow have no posts."}, status=204) # NO CONTENT RESPONSE
            else:
                p = paginate(post_ids, page_num)
                return JsonResponse(p, status=200) # OK RESPONSE
        #check if request is from a user page, return user posts
        elif request.GET.get('page_user'):

            post_ids = list(Post.objects.filter(post_owner__username=request.GET.get('page_user')).values_list("id", flat=True).order_by('-post_creation'))
            if post_ids == []:
                return JsonResponse({"NoPosts": "The user has no posts."}, status=204) # NO CONTENT RESPONSE
            else:
                p = paginate(post_ids, page_num)
                return JsonResponse(p, status=200) # OK RESPONSE

        #else, if resquest is for a feed page, return all posts
        else:
            post_ids = list(Post.objects.all().values_list("id", flat=True).order_by('-post_creation'))
            p = paginate(post_ids, page_num)
            return JsonResponse(p, status=200) # OK RESPONSE

# API TO FETCH A POST INFO, GET PARAMETER REQUIRED (?post_id=)
def get_post_info(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required."}, status=400) # BAD REQUEST RESPONSE
    else:
        post_id = request.GET.get('post_id')
        post_info = list(Post.objects.filter(id=post_id).values('post_owner__username', 'post_owner__image', 'post_content', 'post_creation__date', 'post_creation__time'))
        post_info = post_info[0]
        post_info["post_creation__time"] = post_info["post_creation__time"].strftime("%H:%M")

        #calculate post likes
        post_likes = Post.objects.filter(id=post_id).values_list('post_likes', flat=True)
        if post_likes[0] == None: post_likes = []
        post_info["post_likes"] = len(post_likes)
        post_info["post_id"] = post_id
        
        #determine if post is liked by the user
        if Like.objects.filter(like_post_id=post_id, like_user_id=request.user.id):
            post_info["post_liked"] = True
        else:
            post_info["post_liked"] = False

        return JsonResponse({"post_info": post_info}, status=200) # OK RESPONSE

#API to Follow/Unfollow User
@login_required
def follow_unfollow(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400) # BAD REQUEST RESPONSE
    else:
        username = json.loads(request.body)["username"]
        requester = request.user

        is_followed = a_is_followed_by_b(username, requester)

        if is_followed[0]: #if user is followed by requester
            try:
                Follower.objects.get(id=is_followed[1]).delete()
                return HttpResponse('Unfollowed') #OK RESPONSE
            except Follower.DoesNotExist:
                return HttpResponseNotFound('Could not unfollow user.') #Not Found RESPONSE
        else: #if user is not followed by requester
            try:
                username_id = User.objects.get(username=username).id
                requester_id = User.objects.get(username=requester).id
                new_follow = Follower(user_a_followed_by_b_id=username_id, user_b_follows_a_id=requester_id)
                new_follow.save()
                return HttpResponse('Followed') #OK RESPONSE
            except Follower.DoesNotExist:
                return HttpResponseNotFound('Could not follow user.') #Not Found RESPONSE

#API to Update a Post
def update_post(request):
    if request.method == "POST":
        post_text = json.loads(request.body)["post_text"]
        post_id = json.loads(request.body)["post_id"]

        try:
            post = Post.objects.get(id=post_id)

            #check if user is post owner to update post
            if post.post_owner_id == request.user.id:
                post.post_content = post_text
                post.save()
            return HttpResponse("Post Edited")

        except Post.DoesNotExist:
            return HttpResponseNotFound("Post does not exist. Please try again.")
        except IntegrityError:
            return HttpResponseServerError('Error editing your post. Please try again later.')

    else:
        return HttpResponseBadRequest("Request must be a POST request.")

#API to Like/Dislike a Post
def like_dislike (request):
    if request.method == "POST":
        post_id = json.loads(request.body)["post_id"]
        is_liked = json.loads(request.body)["is_liked"]
        user_id = request.user.id

        # check if post is liked by user
        
        try:
            #post is already liked and user clicked to dislike
            if Like.objects.filter(like_post_id=post_id, like_user_id=user_id) and is_liked:
                Like.objects.get(like_post_id=post_id, like_user_id=user_id).delete()
                return HttpResponse("post_disliked")

            
            #post is not liked and user clicked to like
            elif not is_liked:
                like = Like(like_post_id=post_id, like_user_id=user_id)
                like.save()
                return HttpResponse("post_liked")



        
        except Like.DoesNotExist:
            return HttpResponseNotFound("Like does not exist. Please try again.")
        except IntegrityError:
            return HttpResponseServerError("Could not like post.")

    
    else:
        return HttpResponseBadRequest("Request must be a POST request.")
