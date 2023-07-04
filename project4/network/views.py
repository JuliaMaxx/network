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


def index(request):
    if request.method == "GET":
        posts = Post.objects.all()
        posts = posts.order_by('-time')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {
            "posts": page_obj
        })
    elif 'post' in request.POST:
        post = request.POST['post']
        new_post = Post(user=request.user, text=post)
        new_post.save()
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def edit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        text = data.get('edited', '')
        pk = data.get('id', '')
        post = Post.objects.get(pk=pk)
        post.text = text
        post.save()
        return JsonResponse({"message": "Post edited successfully."}, status=201)

def edited(request, id):
    post = Post.objects.get(pk=id)
    data = {'text':post.text}
    return JsonResponse(data, safe=False)

@csrf_exempt
def likes(request, id, user_id):
    user = User.objects.get(pk=user_id)
    post = Post.objects.get(pk=id)
    if request.method == 'GET':
        liked = False
        for like in user.liked.all():
            if post == like.post:
                liked = True
                break
        likes = post.likes.count()
        data = {'likes':likes, 'liked':liked}
        return JsonResponse(data, safe=False)
    elif request.method == 'PUT':
        like = Like.objects.filter(user=user, post=post)
        like.delete()
        return JsonResponse({"message": "Like removed successfully."}, status=201)
    else:
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
    user = User.objects.get(pk=profile_id)
    posts = user.posts.order_by('-time')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == 'GET':
        return render(request, "network/profile.html", {
            "user1":user, "posts": page_obj
        })
    else:
        if request.POST['followers'] == 'follow':
            user.followers.add(request.user)
            user.save()
        else:
            user.followers.remove(request.user)
            user.save()
        return HttpResponseRedirect(reverse("profile", args=(user.id, )))
    
@login_required
def following(request, profile_id):
    user = User.objects.get(pk=profile_id)
    following = user.following.all()
    posts = []
    for followed_user in following:
       posts += followed_user.posts.order_by('-time')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render (request, "network/following.html", {"posts":page_obj})