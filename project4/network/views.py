from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Post, Like
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from itertools import chain


def index(request):
    if request.method == "GET":
        # get all the posts
        posts = Post.objects.all()
        # order posts in reverse-chronological order
        posts = posts.order_by('-time')
        # set up pagination by 10
        paginator = Paginator(posts, 10)
        # get the number of the page in the url
        page_number = request.GET.get('page')
        # get current page's posts
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "posts": page_obj
        })
    elif 'post' in request.POST:
        # add a new post to the database
        post = request.POST['post']
        new_post = Post(user=request.user, text=post)
        new_post.save()
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def edit(request):
    if request.method == "POST":
        # edit post using json
        data = json.loads(request.body)
        text = data.get('edited', '')
        pk = data.get('id', '')
        post = Post.objects.get(pk=pk)
        post.text = text
        post.save()
        return JsonResponse({"message": "Post edited successfully."}, status=201)

def edited(request, id):
    # get edited post using json
    post = Post.objects.get(pk=id)
    data = {'text':post.text}
    return JsonResponse(data, safe=False)

@csrf_exempt
def likes(request, id, user_id):
    # get the user by id
    user = User.objects.get(pk=user_id)
    # get the post by id
    post = Post.objects.get(pk=id)
    if request.method == 'GET':
        liked = False
        # find out if the user liked the post
        for like in user.liked.all():
            if post == like.post:
                liked = True
                break
        # count the number of likes a post has
        likes = post.likes.count()
        # send the data using json
        data = {'likes':likes, 'liked':liked}
        return JsonResponse(data, safe=False)
    elif request.method == 'PUT':
        # delete like 
        like = Like.objects.filter(user=user, post=post)
        like.delete()
        return JsonResponse({"message": "Like removed successfully."}, status=201)
    else:
        # add like
        like = Like(user=user, post=post)
        like.save()
        return JsonResponse({"message": "Liked successfully."}, status=201)

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
        if request.FILES['image']:
            image = request.FILES["image"]

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
            if image:
                user.image = image
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
    
def profile(request, profile_id):
    # get user
    user = User.objects.get(pk=profile_id)
    # get posts ordered in reverse-chronological order
    posts = user.posts.order_by('-time')
    # set up pagination by 10
    paginator = Paginator(posts, 10)
    # get the page number in the url
    page_number = request.GET.get('page')
    # get current page's posts
    page_obj = paginator.get_page(page_number)
    if request.method == 'GET':
        return render(request, "network/profile.html", {
            "user1":user, "posts": page_obj
        })
    else:
        if request.POST['followers'] == 'follow':
            # follow
            user.followers.add(request.user)
            user.save()
        else:
            # unfollow
            user.followers.remove(request.user)
            user.save()
        return HttpResponseRedirect(reverse("profile", args=(user.id, )))
    
@login_required
def following(request, profile_id):
    # get the user
    user = User.objects.get(pk=profile_id)
    # get all the followed users
    following = user.following.all()
    # get all the posts in the reverse-chronological order
    posts = Post.objects.filter(user__in=following).order_by('-time')
    # set up paginator
    paginator = Paginator(posts, 10)
    # get the page number from url
    page_number = request.GET.get('page')
    # get current page's posts
    page_obj = paginator.get_page(page_number)
    return render (request, "network/following.html", {"posts":page_obj})